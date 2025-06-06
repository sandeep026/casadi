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


      #include "superscs_interface.hpp"
      #include <string>

      const std::string casadi::SuperscsInterface::meta_doc=
      "\n"
"\n"
"\n"
"Interface to the SuperSCS solver for conic programming\n"
"\n"
"Joris Gillis, 2019\n"
"\n"
"Extra doc: https://github.com/casadi/casadi/wiki/L_21z \n"
"\n"
"\n"
">List of available options\n"
"\n"
"+----------+---------+-----------------------------------+\n"
"|    Id    |  Type   |            Description            |\n"
"+==========+=========+===================================+\n"
"| superscs | OT_DICT | Options to be passed to superscs. |\n"
"+----------+---------+-----------------------------------+\n"
"\n"
"\n"
"\n"
"\n"
;
