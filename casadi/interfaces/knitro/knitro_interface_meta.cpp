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


      #include "knitro_interface.hpp"
      #include <string>

      const std::string casadi::KnitroInterface::meta_doc=
      "\n"
"\n"
"\n"
"KNITRO interface\n"
"\n"
"Extra doc: https://github.com/casadi/casadi/wiki/L_22c \n"
"\n"
"\n"
">List of available options\n"
"\n"
"+--------------------------+--------------------+--------------------------+\n"
"|            Id            |        Type        |       Description        |\n"
"+==========================+====================+==========================+\n"
"| complem_variables        | OT_INTVECTORVECTOR | List of complementary    |\n"
"|                          |                    | constraints on simple    |\n"
"|                          |                    | bounds. Pair (i, j)      |\n"
"|                          |                    | encodes complementarity  |\n"
"|                          |                    | between the bounds on    |\n"
"|                          |                    | variable i and variable  |\n"
"|                          |                    | j.                       |\n"
"+--------------------------+--------------------+--------------------------+\n"
"| contype                  | OT_INTVECTOR       | Type of constraint       |\n"
"+--------------------------+--------------------+--------------------------+\n"
"| detect_linear_constraint | OT_BOOL            | Detect type of           |\n"
"| s                        |                    | constraints              |\n"
"+--------------------------+--------------------+--------------------------+\n"
"| knitro                   | OT_DICT            | Options to be passed to  |\n"
"|                          |                    | KNITRO                   |\n"
"+--------------------------+--------------------+--------------------------+\n"
"| options_file             | OT_STRING          | Read options from file   |\n"
"|                          |                    | (solver specific)        |\n"
"+--------------------------+--------------------+--------------------------+\n"
"\n"
"\n"
"\n"
"\n"
;
