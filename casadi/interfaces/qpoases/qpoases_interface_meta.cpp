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


      #include "qpoases_interface.hpp"
      #include <string>

      const std::string casadi::QpoasesInterface::meta_doc=
      "\n"
"\n"
"\n"
"Interface to QPOases Solver for quadratic programming \n"
"\n"
"::\n"
"\n"
"  Extra doc: https://github.com/casadi/casadi/wiki/L_22o \n"
"  \n"
"\n"
"\n"
"\n"
"\n"
">List of available options\n"
"\n"
"+-------------------------------+-----------+------------------------------+\n"
"|              Id               |   Type    |         Description          |\n"
"+===============================+===========+==============================+\n"
"| CPUtime                       | OT_DOUBLE | The maximum allowed CPU time |\n"
"|                               |           | in seconds for the whole     |\n"
"|                               |           | initialisation (and the      |\n"
"|                               |           | actually required one on     |\n"
"|                               |           | output). Disabled if unset.  |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| boundRelaxation               | OT_DOUBLE | Initial relaxation of bounds |\n"
"|                               |           | to start homotopy and        |\n"
"|                               |           | initial value for far        |\n"
"|                               |           | bounds.                      |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| boundTolerance                | OT_DOUBLE | If upper and lower bounds    |\n"
"|                               |           | differ less than this        |\n"
"|                               |           | tolerance, they are regarded |\n"
"|                               |           | equal, i.e. as equality      |\n"
"|                               |           | constraint.                  |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableCholeskyRefactorisation | OT_INT    | Specifies the frequency of a |\n"
"|                               |           | full re-factorisation of     |\n"
"|                               |           | projected Hessian matrix: 0: |\n"
"|                               |           | turns them off, 1: uses them |\n"
"|                               |           | at each iteration etc.       |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableDriftCorrection         | OT_INT    | Specifies the frequency of   |\n"
"|                               |           | drift corrections: 0: turns  |\n"
"|                               |           | them off.                    |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableEqualities              | OT_BOOL   | Specifies whether equalities |\n"
"|                               |           | should be treated as always  |\n"
"|                               |           | active (True) or not (False) |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableFarBounds               | OT_BOOL   | Enables the use of far       |\n"
"|                               |           | bounds.                      |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableFlippingBounds          | OT_BOOL   | Enables the use of flipping  |\n"
"|                               |           | bounds.                      |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableFullLITests             | OT_BOOL   | Enables condition-hardened   |\n"
"|                               |           | (but more expensive) LI      |\n"
"|                               |           | test.                        |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableInertiaCorrection       | OT_BOOL   | Should working set be        |\n"
"|                               |           | repaired when negative       |\n"
"|                               |           | curvature is discovered      |\n"
"|                               |           | during hotstart.             |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableNZCTests                | OT_BOOL   | Enables nonzero curvature    |\n"
"|                               |           | tests.                       |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableRamping                 | OT_BOOL   | Enables ramping.             |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| enableRegularisation          | OT_BOOL   | Enables automatic Hessian    |\n"
"|                               |           | regularisation.              |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| epsDen                        | OT_DOUBLE | Denominator tolerance for    |\n"
"|                               |           | ratio tests.                 |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| epsFlipping                   | OT_DOUBLE | Tolerance of squared         |\n"
"|                               |           | Cholesky diagonal factor     |\n"
"|                               |           | which triggers flipping      |\n"
"|                               |           | bound.                       |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| epsIterRef                    | OT_DOUBLE | Early termination tolerance  |\n"
"|                               |           | for iterative refinement.    |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| epsLITests                    | OT_DOUBLE | Tolerance for linear         |\n"
"|                               |           | independence tests.          |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| epsNZCTests                   | OT_DOUBLE | Tolerance for nonzero        |\n"
"|                               |           | curvature tests.             |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| epsNum                        | OT_DOUBLE | Numerator tolerance for      |\n"
"|                               |           | ratio tests.                 |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| epsRegularisation             | OT_DOUBLE | Scaling factor of identity   |\n"
"|                               |           | matrix used for Hessian      |\n"
"|                               |           | regularisation.              |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| finalRamping                  | OT_DOUBLE | Final value for ramping      |\n"
"|                               |           | strategy.                    |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| growFarBounds                 | OT_DOUBLE | Factor to grow far bounds.   |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| hessian_type                  | OT_STRING | Type of Hessian - see        |\n"
"|                               |           | qpOASES documentation [UNKNO |\n"
"|                               |           | WN|posdef|semidef|indef|zero |\n"
"|                               |           | |identity]]                  |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| initialFarBounds              | OT_DOUBLE | Initial size for far bounds. |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| initialRamping                | OT_DOUBLE | Start value for ramping      |\n"
"|                               |           | strategy.                    |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| initialStatusBounds           | OT_STRING | Initial status of bounds at  |\n"
"|                               |           | first iteration.             |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| linsol_plugin                 | OT_STRING | Linear solver plugin         |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| maxDualJump                   | OT_DOUBLE | Maximum allowed jump in dual |\n"
"|                               |           | variables in linear          |\n"
"|                               |           | independence tests.          |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| maxPrimalJump                 | OT_DOUBLE | Maximum allowed jump in      |\n"
"|                               |           | primal variables in nonzero  |\n"
"|                               |           | curvature tests.             |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| max_schur                     | OT_INT    | Maximal number of Schur      |\n"
"|                               |           | updates [75]                 |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| nWSR                          | OT_INT    | The maximum number of        |\n"
"|                               |           | working set recalculations   |\n"
"|                               |           | to be performed during the   |\n"
"|                               |           | initial homotopy. Default is |\n"
"|                               |           | 5(nx + nc)                   |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| numRefinementSteps            | OT_INT    | Maximum number of iterative  |\n"
"|                               |           | refinement steps.            |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| numRegularisationSteps        | OT_INT    | Maximum number of successive |\n"
"|                               |           | regularisation steps.        |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| printLevel                    | OT_STRING | Defines the amount of text   |\n"
"|                               |           | output during QP solution,   |\n"
"|                               |           | see Section 5.7              |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| schur                         | OT_BOOL   | Use Schur Complement         |\n"
"|                               |           | Approach [false]             |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| sparse                        | OT_BOOL   | Formulate the QP using       |\n"
"|                               |           | sparse matrices. [false]     |\n"
"+-------------------------------+-----------+------------------------------+\n"
"| terminationTolerance          | OT_DOUBLE | Relative termination         |\n"
"|                               |           | tolerance to stop homotopy.  |\n"
"+-------------------------------+-----------+------------------------------+\n"
"\n"
"\n"
"\n"
"\n"
;
