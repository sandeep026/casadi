#pragma once

#include "type-erased-solver-stats.hpp"

namespace alpaqa {

template <Config Conf>
struct InnerSolverVTable : util::BasicVTable {
    USING_ALPAQA_CONFIG(Conf);
    using Stats = TypeErasedInnerSolverStats<Conf>;

    Stats (*call)(void *, const ProblemBase<Conf> &, crvec, real_t, bool, rvec, rvec,
                  rvec)                   = nullptr;
    void (*stop)(void *)                  = nullptr;
    std::string (*get_name)(const void *) = nullptr;

    template <class T>
    InnerSolverVTable(util::VTableTypeTag<T> t) : util::BasicVTable{t} {
        stop     = util::type_erased_wrapped<&T::stop>();
        get_name = util::type_erased_wrapped<&T::get_name>();
        call     = [](void *self, const ProblemBase<Conf> &p, auto... valargs) {
            constexpr auto call = util::type_erased_wrapped<&T::operator()>();
            return Stats{call(self, p, valargs...)};
        };
    }
    InnerSolverVTable() = default;
};

template <Config Conf = DefaultConfig, class Allocator = std::allocator<std::byte>>
class TypeErasedInnerSolver : util::TypeErased<InnerSolverVTable<Conf>, Allocator> {
  public:
    USING_ALPAQA_CONFIG(Conf);
    using VTable         = InnerSolverVTable<Conf>;
    using allocator_type = Allocator;
    using TypeErased     = util::TypeErased<VTable, allocator_type>;
    using Stats          = typename VTable::Stats;
    using TypeErased::TypeErased;

  private:
    using TypeErased::self;
    using TypeErased::vtable;

  public:
    template <class T, class... Args>
    static TypeErasedInnerSolver make(Args &&...args) {
        return TypeErased::template make<TypeErasedInnerSolver, T>(std::forward<Args>(args)...);
    }

    template <class... Args>
    decltype(auto) operator()(Args &&...args) {
        return vtable.call(self, std::forward<Args>(args)...);
    }
    template <class... Args>
    decltype(auto) stop(Args &&...args) {
        return vtable.stop(self, std::forward<Args>(args)...);
    }
    template <class... Args>
    decltype(auto) get_name(Args &&...args) const {
        return vtable.get_name(self, std::forward<Args>(args)...);
    }
};

} // namespace alpaqa