/*
 *    This file is part of CasADi.
 *
 *    CasADi -- A symbolic framework for dynamic optimization.
 *    Copyright (C) 2010-2023 Joel Andersson, Joris Gillis, Moritz Diehl,
 *                            KU Leuven. All rights reserved.
 *    Copyright (C) 2011-2014 Greg Horn
 *
 *    CasADi is free software; you can redistribute it and/or
 *    modify it under the terms of the GNU Lesser General Public
 *    License as published by the Free Software Foundation; either
 *    version 3 of the License, or (at your option) any later version.
 *
 *    CasADi is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *    Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public
 *    License along with CasADi; if not, write to the Free Software
 *    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */


      #include "highs_interface.hpp"
      #include <string>

      const std::string casadi::HighsInterface::meta_doc=
      "\n"
"\n"
"\n"
"Interface to HiGHS solver for sparse Quadratic Programs, see \n"
"highs.dev for more information and https://www.maths.ed.ac.uk/hall/HiGHS/HighsOptions.html  for a list of options.\n"
"\n"
"Extra doc: https://github.com/casadi/casadi/wiki/L_29k \n"
"\n"
"\n"
">List of available options\n"
"\n"
"+-------+---------+--------------------------------+\n"
"|  Id   |  Type   |          Description           |\n"
"+=======+=========+================================+\n"
"| highs | OT_DICT | Options to be passed to HiGHS. |\n"
"+-------+---------+--------------------------------+\n"
"\n"
"\n"
"\n"
"\n"
;
