#include <panoc-alm/decl/alm.hpp>
#include <panoc-alm/inner/decl/panoc.hpp>
#include <panoc-alm/inner/lbfgs.hpp>

#include <panoc-alm/interop/cutest/CUTEstLoader.hpp>

#include <drivers/YAMLEncoder.hpp>

#include <atomic>
#include <chrono>
#include <csignal>
#include <fstream>
#include <iostream>
#include <sstream>

using namespace std::chrono_literals;

#if 0
#include <panoc-alm/alm.hpp>
#include <panoc-alm/inner/panoc.hpp>
#include <panoc-alm/inner/specialized-lbfgs.hpp>
using Solver = pa::ALMSolver<pa::PANOCSolver<pa::SpecializedLBFGS>>;
#else
using Solver = pa::ALMSolver<>;
#endif

std::atomic<Solver *> acitve_solver{nullptr};
void signal_callback_handler(int signum) {
    if (signum == SIGINT) {
        if (auto *s = acitve_solver.load(std::memory_order_relaxed)) {
            std::atomic_signal_fence(std::memory_order_acquire);
            s->stop();
        }
    }
}

int main(int argc, char *argv[]) {
    using namespace std::string_literals;
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <problem name> <output folder>"
                  << std::endl;
        return 1;
    }
    std::string prob_dir = "CUTEst/"s + argv[1];
    CUTEstProblem cp(prob_dir + "/libcutest-problem-" + argv[1] + ".so",
                     prob_dir + "/OUTSDIF.d");

    pa::ALMParams almparams;
    almparams.max_iter        = 200;
    almparams.max_time        = 1min + 30s;
    almparams.preconditioning = false;
    // almparams.print_interval  = 1;
    // almparams.Σ₀ = 1e-2;
    // almparams.ε₀ = 1e-5;
    // almparams.Δ = 1.1;
    pa::PANOCParams panocparams;
    panocparams.max_iter                       = 1000;
    panocparams.update_lipschitz_in_linesearch = true;
    panocparams.lbfgs_mem                      = 20;
    // panocparams.print_interval = 500;

    pa::LBFGSParams lbfgsparams;

    Solver solver{almparams, {panocparams, lbfgsparams}};
    std::atomic_signal_fence(std::memory_order_release);
    acitve_solver.store(&solver, std::memory_order_relaxed);
    signal(SIGINT, signal_callback_handler);

    auto problem = pa::ProblemWithCounters(cp.problem);

    auto status = solver(problem, cp.y0, cp.x0);
    // ??? TODO: fence
    acitve_solver.store(nullptr, std::memory_order_relaxed);
    // ??? TODO: fence
    auto report = cp.get_report();

    auto f_star = cp.problem.f(cp.x0);

    YAML::Emitter out;
    out << YAML::BeginMap;
    out << YAML::Key << "solver" << YAML::Value << solver.get_name();
    out << YAML::Key << "status" << YAML::Value << status.status;
    out << YAML::Key << "outer iterations" << YAML::Value
        << status.outer_iterations;
    out << YAML::Key << "inner iterations" << YAML::Value
        << status.inner_iterations;
    out << YAML::Key << "inner convergence failures" << YAML::Value
        << status.inner_convergence_failures;
    out << YAML::Key << "elapsed time" << YAML::Value
        << std::chrono::duration<double>(status.elapsed_time).count();
    out << YAML::Key << "ε" << YAML::Value << status.ε;
    out << YAML::Key << "δ" << YAML::Value << status.δ;
    out << YAML::Key << "f" << YAML::Value << f_star;
    out << YAML::Key << "counters" << YAML::Value << problem.evaluations;
    out << YAML::Key << "linesearch failures" << YAML::Value
        << status.inner_linesearch_failures;
    out << YAML::Key << "L-BFGS failures" << YAML::Value
        << status.inner_lbfgs_failures;
    out << YAML::Key << "L-BFGS rejected" << YAML::Value
        << status.inner_lbfgs_rejected;
    out << YAML::Key << "‖Σ‖" << YAML::Value << status.norm_penalty;
    out << YAML::Key << "‖x‖" << YAML::Value << cp.x0.norm();
    out << YAML::Key << "‖y‖" << YAML::Value << cp.y0.norm();
    // out << YAML::Key << "x" << YAML::Value << cp.x0;
    // out << YAML::Key << "y" << YAML::Value << cp.y0;
    out << YAML::EndMap;
    // out << report;

    std::ofstream(argv[2] + "/"s + argv[1] + ".yaml")
        << out.c_str() << std::endl;

    std::cout << out.c_str() << std::endl;
}