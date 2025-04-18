#
#     This file is part of CasADi.
#
#     CasADi -- A symbolic framework for dynamic optimization.
#     Copyright (C) 2010-2023 Joel Andersson, Joris Gillis, Moritz Diehl,
#                             KU Leuven. All rights reserved.
#     Copyright (C) 2011-2014 Greg Horn
#
#     CasADi is free software; you can redistribute it and/or
#     modify it under the terms of the GNU Lesser General Public
#     License as published by the Free Software Foundation; either
#     version 3 of the License, or (at your option) any later version.
#
#     CasADi is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#     Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public
#     License along with CasADi; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#

import casadi as c
import numpy
from numpy import random, array, linalg, matrix, zeros, ones
import unittest
from types import *
from helpers import *
from casadi import *

scipy_available = True
try:
	from scipy.sparse import csc_matrix
except:
	scipy_available = False
import warnings

inherit_from = object

 
if has_nlpsol("ipopt"):
  inherit_from = casadiTestCase
  nlpsolver = "ipopt"
  nlpsolver_options = {}

class OptiStacktests(inherit_from):


    @requires_conic("qrqp")
    def test_conic(self):
      opti = Opti('conic')
      x = opti.variable(2)
      opti.minimize(dot(x,x))
      opti.subject_to(x[0]>=2)
      opti.subject_to(x[1]>=3)
      opti.solver('qrqp')

      sol = opti.solve()
      self.checkarray(sol.value(x),vertcat(2,3))

      with self.assertInException("conic"):
        Opti('foo')


    def test_lookup(self):
      opti = Opti()
      x = opti.variable(2)
      y = opti.variable(2)
      opti.subject_to(x>=y)

      str0 = str(opti.debug.x_lookup(0))
      str1 = str(opti.debug.x_lookup(1))
      str2 = str(opti.debug.x_lookup(2))
      str3 = str(opti.debug.x_lookup(3))
      
      self.assertEqual(str0,str1)
      self.assertEqual(str2,str3)
      
      self.assertFalse(str1==str2)
     
      
      
    def test_n(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y**2)**2)
      opti.subject_to(x+y>=1)
      opti.subject_to(z+x>=1)
      
      opti.solver('ipopt')
      sol = opti.solve()

      self.assertEqual(sol.opti.nx,3)
      self.assertEqual(sol.opti.ng,2)
      self.assertEqual(sol.opti.np,0)
      
    def test_subject_to_list(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y**2)**2)
      opti.subject_to([x+y>=1,z+x>=1])
      
      opti.solver('ipopt')
      sol = opti.solve()

      self.assertEqual(sol.opti.nx,3)
      self.assertEqual(sol.opti.ng,2)
      self.assertEqual(sol.opti.np,0)
      
    def test_sol_opti(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y**2)**2)
      opti.subject_to(x+y>=1)
      opti.subject_to(z+x>=1)
      
      opti.solver(nlpsolver,nlpsolver_options)

      sol = opti.solve()
      
      sol.opti.nx
      
    def test_to_function(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      p = opti.parameter()
      
      opti.minimize(y**2+sin(x-y-p)**2)
      opti.subject_to(x+y>=1)

      opti.solver(nlpsolver,nlpsolver_options)

      

      F = opti.to_function("F",[x,p,opti.lam_g],[x,y])
      
      r = F(0,0.1,0)
      
      print(F(0.1,0.1,0))
      print(F(0,2,0))
      print(F(100,1,0))

      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      p = opti.parameter()

      opti.minimize(sin(2*pi*(x+y-p))**2+sin(pi*z)**2)
      opti.subject_to(x==2*y)

      opti.solver("ipopt")

      F = opti.to_function("F",[vertcat(x,y,z),p],[vertcat(x,y,z)])

      self.checkarray(F([3.9,1.8,0],6),vertcat(4,2,0))
      self.checkarray(F([0,1,0],6),vertcat(2.0/3,1.0/3,0))
      self.checkarray(F([3.9,1.8,7.8],6),vertcat(4,2,8))
      self.checkarray(F([0,1,7.8],6),vertcat(2.0/3,1.0/3,8))

      F = opti.to_function("F",[vertcat(z,x,y),p],[vertcat(x,y,z)])
      self.checkarray(F([7.8,3.9,1.8],6),vertcat(4,2,8))
      self.checkarray(F([7.8,0,1],6),vertcat(2.0/3,1.0/3,8))


      b = opti.variable()
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      a = opti.variable()
      p = opti.parameter()

      opti.minimize(sin(2*pi*(x+y-p))**2+sin(pi*z)**2)
      opti.subject_to(x==2*y)

      opti.solver("ipopt")

      with self.assertInException("Argument 0"):
        opti.to_function("F",[vertcat(x,2)],[vertcat(x,y,z)])
      with self.assertInException("Argument 1"):
        opti.to_function("F",[y,vertcat(x,2)],[vertcat(x,y,z)])

      with self.assertInException("not independent"):
        opti.to_function("F",[x,x],[vertcat(x,y,z)])
      opti.to_function("F",[a],[vertcat(x,y,z)])
      with self.assertInException("belonging to a different instance"):
        opti.to_function("F",[b],[vertcat(x,y,z)])

    def test_dual(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y**2)**2)
      opti.subject_to(x+y>=1)
      opti.subject_to(z+x>=1)
      
      opti.solver(nlpsolver,nlpsolver_options)

      sol = opti.solve()
      
 

    def test_sparse(self):
      opti = Opti()
      x = opti.variable(3,1)
      p = opti.parameter()

      opti.minimize((p*x[1]-x[0]**2)**2)
      opti.subject_to(x[0]+3*x[1]==1)
      
      opti.solver(nlpsolver,nlpsolver_options)
      opti.set_value(p, 3)
      
      sol = opti.solve()
      
      if scipy_available:
        self.assertTrue(isinstance(sol.value(DM.eye(3)),csc_matrix))

    def test_structure(self):
      opti = Opti()
      x = opti.variable(3,1)
      p = opti.parameter()

      opti.minimize((p*x[1]-x[0]**2)**2)
      opti.subject_to(x[0]+3*x[1]==1)
      
      opti.solver(nlpsolver,nlpsolver_options)
      opti.set_value(p, 3)

      sol = opti.solve()
      
      jac_g = jacobian(opti.g,opti.x)
      self.checkarray(sol.value(jac_g),sol.value(sol.opti.debug.casadi_solver.get_function('nlp_jac_g')(opti.x,opti.p)[1]))
      grad_f = gradient(opti.f,opti.x)
      self.checkarray(sol.value(grad_f),sol.value(sol.opti.debug.casadi_solver.get_function('nlp_grad_f')(opti.x,opti.p)[1]))
      hess_lag = sol.value(hessian(opti.f+dot(opti.lam_g,opti.g),opti.x)[0])
      self.checkarray(sol.value(hess_lag),sol.value(tril2symm(sol.opti.debug.casadi_solver.get_function('nlp_hess_l')(opti.x,opti.p,1,opti.lam_g).T)))


    def test_warmstart(self):
      opti = Opti()

      x = opti.variable(2,1)
      p = opti.parameter()

      opti.minimize((p*x[1]-x[0]**2)**2)
      opti.subject_to(x[0]+3*x[1]==1)

      opti.solver(nlpsolver,nlpsolver_options)

      opti.set_value(p, 3)
      sol = opti.solve()
      
      sol1 = sol

      opti.set_value(p, 4)
      sol = opti.solve()
      
      with self.assertRaises(Exception):
        self.checkarray(sol.value(x),sol1.value(x))
      
      it = sol.stats()["iter_count"]
      
      self.assertTrue(it!=0)
      sol = opti.solve()
      self.assertTrue(sol.stats()["iter_count"]==it)
      
      opti.set_initial(sol.value_variables())
      sol = opti.solve()
      
      self.assertTrue(sol.stats()["iter_count"]!=it)
      opti.set_value(sol1.value_parameters())
      sol = opti.solve()
      self.checkarray(sol.value(x),sol1.value(x), digits=6)
      
      
    def test_set_value_expr(self):

      opti = Opti()
      p = opti.parameter(3,1)
      v = opti.parameter(2,1)
      x = opti.variable(2)
      
      opti.set_value(p, 0)
      opti.set_value(v, 0)
      opti.set_value(p[0], 3)
      self.checkarray(opti.debug.value(p),vertcat(3,0,0))
      opti.set_value(p[[0,2]], 2)
      self.checkarray(opti.debug.value(p),vertcat(2,0,2)) 
      opti.set_value(p[[0,2]], [1,2])
      self.checkarray(opti.debug.value(p),vertcat(1,0,2)) 
      opti.set_value(p[[2,0]], [1,2])
      self.checkarray(opti.debug.value(p),vertcat(2,0,1)) 

      opti.set_value(veccat(v,p), [1,2,3,4,5])
      self.checkarray(opti.debug.value(p),vertcat(3,4,5))
      self.checkarray(opti.debug.value(v),vertcat(1,2))    
     
     
      opti.set_value(p, 0)
      opti.set_value(veccat(p[0],p[0]), [4,4])
      self.checkarray(opti.debug.value(p),vertcat(4,0,0))
      with self.assertInException("ambiguous"):
        opti.set_value(veccat(p[0],p[0]), [4,5])
      with self.assertInException("cannot set a value for a variable"):
        opti.set_value(veccat(p,x,v), [4,5])
      opti.set_value(p, 0)
      opti.set_value(3*p[0], 3)
      self.checkarray(opti.debug.value(p),vertcat(1,0,0))
      with self.assertInException("cannot set initial/value of an arbitrary expression"):
        opti.set_value(p[0]+p[1], 3)

      opti.set_value(veccat(v,3), [1,2,3])
      opti.set_value(veccat(2,v,5,p), [2,3,4,5,6,7,8])
      opti.set_value(veccat(2,v,5,p,v), [2,3,4,5,6,7,8,3,4])
      
      with self.assertInException("inconsistent"):
        opti.set_value(veccat(v,3), [1,2,4])
      with self.assertInException("inconsistent"):
        opti.set_value(veccat(2,v,5,p), [5,3,4,2,6,7,8])
      with self.assertInException("ambiguous"):
        opti.set_value(veccat(2,v,5,p,v), [2,3,4,5,6,7,8,4,3])
          
    def test_shapes(self):
        
          opti = Opti()
          
          F = opti.variable(10,1)
          x = opti.variable(2,11)
         
          opti.subject_to(x[:,0]==x[:,1]) 
          opti.subject_to(opti.bounded(-1,F,1))

          opti.solver(nlpsolver,nlpsolver_options)
          opti.minimize(sum1(F))
          sol = opti.solve()

    def test_symb_boundedshapes(self):
        
          opti = Opti()
          
          y = opti.variable()
          x = opti.variable()
         
          opti.subject_to(opti.bounded(0,y,x))

          opti.solver(nlpsolver,nlpsolver_options)
          opti.minimize(x**2+(y-6)**2)
          
          opti.subject_to(x<=3)
          sol = opti.solve()
          
          self.checkarray(sol.value(y), 3, digits=3)

    def test_symb_parametric(self):
        
          opti = Opti()
          
          y = opti.parameter(3,1)
          x = opti.parameter(3,1)
         
          with self.assertInException("!parametric[0]"):
            opti.subject_to(x<=y)

          
    def test_callback(self):
        
          opti = Opti()
          
          eps = 1e-5 
          
          x = opti.variable()
          y = opti.variable()
          
          p = opti.parameter()
          
          opti.minimize((x-1)**4+(y-p)**4)
          opti.solver(nlpsolver,nlpsolver_options)

          opti.callback(lambda i: ret.setdefault('a',opti.debug.value(p)))
          opti.set_value(p, 3)
          ret = {}
          sol = opti.solve()

          self.assertTrue(ret['a']==3)
          opti.set_value(p, 2)
          ret = {}
          sol = opti.solve()
          self.assertTrue(ret['a']==2)
          opti.set_value(p, 3)
          ret = {}
          sol = opti.solve()
          self.assertTrue(ret['a']==3)
          
          opti.callback()
          ret = {}
          sol = opti.solve()
          self.assertFalse('a' in ret)

          opti.callback(lambda i: ret.setdefault('b',opti.debug.value(p)))
          sol = opti.solve()
          self.assertTrue(ret['b']==3)
          
          
          opti = opti.copy()
          ret = {}
          sol = opti.solve()
          self.assertTrue(len(ret)==0)

    def test_debug_value(self):
      
        opti = Opti()
        p = opti.parameter()
        opti.set_value(p, 3)
        self.checkarray(opti.debug.value(p**2), 9)
        x = opti.variable()
        
        with self.assertInException("This action is forbidden since you have not solved the Opti stack yet"):
          opti.debug.value(x**2)
        
        with self.assertInException("You cannot set a value for a variable"):
          opti.set_value(x, 2)
        with self.assertInException("You cannot set a value for a variable"):
          opti.set_value([x==2])
        opti.set_initial(x, 2)
        with self.assertInException("You cannot set an initial value for a parameter"):
          opti.set_initial(p, 2)
        with self.assertInException("You cannot set an initial value for a parameter"):
          opti.set_initial([p==2])
        
        
        with self.assertInException("This action is forbidden since you have not solved the Opti stack yet"):
          opti.debug.value(x**2)
        
        self.checkarray(opti.debug.value(x**2, opti.initial()), 4)
        
        y = opti.variable()
        
        with self.assertInException("This action is forbidden since you have not solved the Opti stack yet"):
          opti.debug.value(x*y)
      
    def test_print(self):
      opti = Opti()
      print(opti)
      self.assertTrue("variables" in str(opti))
      self.assertTrue("variables" in str(opti.debug))
      x = opti.variable()
      y = opti.variable()
      p = opti.parameter()
      print(opti)
      
      opti.minimize((x**2-y)**2)
      print(opti)
      opti.solver(nlpsolver,nlpsolver_options)
      print(opti)
      sol = opti.solve()
      print(sol)
      print(opti)      
            
      opti = Opti()
      print(opti)
      x = opti.variable()
      y = opti.variable()
      
      p = opti.parameter()
      print(opti)
      
      opti.subject_to((x**2-y)**2<=1)
      print(opti)
      opti.solver(nlpsolver,nlpsolver_options)
      print(opti)
      sol = opti.solve()
      print(sol)
      print(opti)
      
      self.assertTrue("variables" in str(sol))
            
    def test_flow(self):
      opti = Opti()
      
      x = opti.variable()
      y = opti.variable()
      
      p = opti.parameter()
      
      w = MX.sym("w")
      
      opti.minimize(x**2)
      opti.solver(nlpsolver,nlpsolver_options)
      sol = opti.solve()
      
      with self.assertInException("do not appear in the constraints and objective"):
        sol.value(y)
      with self.assertInException("decision variable"):
        sol.value(y)
      with self.assertInException("optistack.py"):
        sol.value(y) 
      with self.assertInException("MX symbol 'w' of shape 1x1, declared outside of Opti."):
        sol.value(w)
        
      with self.assertInException("MX symbol 'w' of shape 1x1, declared outside of Opti."):
        opti.subject_to(w<=2)

      with self.assertInException("MX symbol 'w' of shape 1x1, declared outside of Opti."):
        opti.minimize(w)
        
      opti.minimize((x-p)**2)

      with self.assertInException("You have forgotten to assign a value to a parameter"):
        sol = opti.solve()
      with self.assertInException("Opti parameter"):
        sol = opti.solve()
      with self.assertInException("optistack.py"):
        sol = opti.solve()
      opti.set_value(p, 5)
      opti.solve()
      opti.debug.value(x);
      
      opti.set_value(p, 9)
      opti.debug.value(p);
      with self.assertInException("This action is forbidden since you have not solved the Opti stack yet"):
          opti.debug.value(x);
      
      opti.solve()
      opti.set_initial(x, 3)
      opti.debug.value(p);
      with self.assertInException("This action is forbidden since you have not solved the Opti stack yet"):
          opti.debug.value(x);     
      
      con = x>=0
      opti.subject_to(con)
      opti.solve()
            
      opti0 = opti

      opti = Opti()
      
      X = opti.variable()
      y = opti.variable()
      
      P = opti.parameter()
      with self.assertInException("belonging to a different instance of Opti"):
        opti.subject_to(x<=2)

      with self.assertInException("decision variable"):
        opti.subject_to(x<=2)

      with self.assertInException("belonging to a different instance of Opti"):
        opti.subject_to(p<=2)

      with self.assertInException("parameter"):
        opti.subject_to(p<=2)
     
      with self.assertInException("belonging to a different instance of Opti"):
        opti.subject_to(opti0.dual(con)<=2)

      with self.assertInException("dual variable"):
        opti.subject_to(opti0.dual(con)<=2)
        
      con = X>=0
      opti.subject_to(con)
      dual = opti.dual(con)
      
      with self.assertInException("Dual variables forbidden in this context"):
        opti.subject_to(dual>=2)
      with self.assertInException("Dual variables forbidden in this context"):
        opti.minimize(dual)
        
      opti.subject_to()
      opti.minimize(y**2)
      dual = opti.dual(con)
      opti.solver(nlpsolver,nlpsolver_options)
      sol = opti.solve()
      
      with self.assertInException("This expression has a dual for a constraint that is not given to Opti"):
        sol.value(dual)
      with self.assertInException("optistack.py"):
        sol.value(dual)
      
        
        
    def test_simple(self):
      
        opti = Opti()
        
        eps = 1e-5 
        
        x = opti.variable()
        y = opti.variable()
      
        f = (x-1)**2+(y-2)**2  
        opti.minimize(f)

        opti.solver(nlpsolver,nlpsolver_options)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1)
        self.checkarray(sol.value(y), 2)
      

        count = 0
        for con, coneps, xs, ys, mul in [
          (y>=2.5, y+eps>=2.5, 1, 2.5, 1),
          (y>=1.5, y+eps>=1.5, 1, 2, 0),
          (2.5>=y, 2.5+eps>=y, 1, 2, 0),
          (1.5>=y, 1.5+eps>=y, 1, 1.5, 1),
          (y<=2.5, y<=2.5+eps, 1, 2, 0),
          (y<=1.5, y<=1.5+eps, 1, 1.5, 1),
          (2.5<=y, 2.5<=y+eps, 1, 2.5, 1),
          (1.5<=y, 1.5<=y+eps, 1, 2, 0),
          (y>=x,   y+eps>=x, 1, 2, 0),
          (y<=x,   y<=x+eps, 1.5, 1.5, 1),
          (y<=0,   y<=eps, 1, 0, 4),
          ((3<= y) <=4, (3<= y+eps) <=4, 1, 3, None),
          (3<= (y <=4), 3<= (y+eps <=4), 1, 3, None),
          (0<= (y <=1), 0<= (y <=1+eps), 1, 1, None),
          ((0<= y) <=1, (0<= y) <=1+eps, 1, 1, None),
          ((4>= y) >=3, (4>= y+eps) >=3, 1, 3, None),
          ((1>= y) >=0, (1+eps>= y) >=0, 1, 1, None),
          (opti.bounded(3,y,4), opti.bounded(3,y+eps,4), 1, 3, None),
          (opti.bounded(0,y,1), opti.bounded(0,y+eps,1), 1, 1, None)
        
          
          
          ]:
          opti.subject_to()
          opti.subject_to(con)
          sol = opti.solve()
  

          self.checkarray(sol.value(x), xs,digits=7)
          self.checkarray(sol.value(y), ys,digits=7)
        
          dual_value = sol.value(opti.dual(con))
          opti.subject_to()
          opti.subject_to(coneps)
          sol2 = opti.solve()

          s = -sign(sol2.value(f)-sol.value(f))
          
          count+=1
          if mul is not None:
            self.checkarray(dual_value, s*abs(mul),digits=6)
        
        opti.subject_to()
        opti.subject_to(1.5==y)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 1.5,digits=7)
        
        opti.subject_to()
        opti.subject_to(y==1.5)
        sol = opti.solve()
        
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 1.5,digits=7)

        opti.subject_to()
        opti.subject_to(y==x)
        sol = opti.solve()
        
        x = opti.variable(3,3)
        f = trace(x)
        opti.subject_to()
        opti.subject_to(x>=0)
        with self.assertRaises(Exception):
          sol = opti.solve()
        
        x = opti.variable(2,1)
        opti.subject_to()
        opti.minimize((x[0]-1)**2+(x[1]-2)**2)
        opti.subject_to(x[1]>=x[0])
        sol = opti.solve()
        self.checkarray(sol.value(x), vertcat(1,2),digits=7)
          
        opti.subject_to()
        opti.subject_to(x[1]<=x[0])
        sol = opti.solve()
        
        self.checkarray(sol.value(x), vertcat(1.5,1.5),digits=7)
        
        opti.subject_to()
        opti.subject_to(x<=0.5)
        sol = opti.solve()
        
        print("test", sol.value(x))
        self.checkarray(sol.value(x), vertcat(0.5,0.5),digits=7)

    def test_parametric(self):
      
        opti = Opti()
        
        x = opti.variable()
        y = opti.variable()
        p = opti.parameter()
        
        opti.minimize((x-1)**2+(y-p)**2)
        opti.solver(nlpsolver,nlpsolver_options)
        opti.set_value(p, 2)
        sol = opti.solve()

        self.checkarray(sol.value(x), 1)
        self.checkarray(sol.value(y), 2)

        opti.set_value(p, 3)
        sol = opti.solve()


        self.checkarray(sol.value(x), 1)
        self.checkarray(sol.value(y), 3)
        
        opti.minimize((x-1)**2+(y-2)**2)
        
        opti.subject_to()
        opti.subject_to(y>=p)
        opti.set_value(p, 2.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 2.5,digits=7)
        
        opti.set_value(p, 1.5)
        sol = opti.solve()
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 2,digits=7)
        
        opti.subject_to()
        opti.subject_to(p>=y)
        opti.set_value(p, 2.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 2,digits=7)
        
        opti.set_value(p, 1.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 1.5,digits=7)
        
        
        opti.subject_to()
        opti.subject_to(y<=p)
        opti.set_value(p, 2.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 2,digits=7)
        
        opti.set_value(p, 1.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 1.5,digits=7)
        
        opti.subject_to()
        opti.subject_to(p<=y)
        opti.set_value(p, 2.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 2.5,digits=7)
        
        opti.set_value(p, 1.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 2,digits=7)
        
        
        opti.subject_to()
        opti.subject_to(p==y)
        opti.set_value(p, 1.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 1.5,digits=7)
        
        opti.subject_to()
        opti.subject_to(y==p)
        opti.set_value(p, 1.5)
        sol = opti.solve()
        
        self.checkarray(sol.value(x), 1,digits=7)
        self.checkarray(sol.value(y), 1.5,digits=7)
        
    def test_symm(self):
      
        opti = Opti()
        
        P = opti.variable(2, 2, 'symmetric')
        
        R = DM([[1,2],[4,4]])
        
        f = sum2(sum1((P-R)**2))

        x = symvar(f)[0]

        opti.minimize(f)
        opti.solver(nlpsolver,nlpsolver_options)

        sol = opti.solve()
        
        F = casadi.Function('f',[x],[f])

        self.checkarray(sol.value(P), DM([[1,3],[3,4]]))

        P = opti.variable(2, 2)
        
        
        f = sum2(sum1((P-R)**2))

        x = symvar(f)[0]

        
        opti.minimize(f)
        sol = opti.solve()
        
        F = casadi.Function('f',[x],[f])

        self.checkarray(sol.value(P), R)

    def test_broadcast(self):
        opti = Opti()
        
        x = opti.variable(3, 1)
        

        f = mtimes(x.T,x)
        
        opti.minimize(f)
        
        opti.subject_to(x[0]>=vertcat(1,2,3))
        opti.solver(nlpsolver,nlpsolver_options)
        sol = opti.solve()
        self.checkarray(sol.value(x[0]), 3,digits=7)
        

        f = mtimes(x.T,x)
        
        opti.minimize(f)
        
        opti.subject_to();
        
        opti.subject_to(x[0]>=vertcat(1+x[1],0.5,0))
        opti.solver(nlpsolver,nlpsolver_options)
        sol = opti.solve()
        self.checkarray(sol.value(x[0]), 0.5,digits=4)

    def test_constraint_dim_mismatch(self):
        opti = Opti()
        x = opti.variable(5,1)

        p = opti.parameter(1,1)
        q = opti.parameter(1,1)


        opti.minimize(dot(x,x))
        with self.assertInException("Constraint must contain decision variables."):
          opti.subject_to(p==q)
        with self.assertInException("Constraint shape mismatch."):
          opti.subject_to(x[0]==vertcat(1,2,3))
        with self.assertInException("Constraint shape mismatch."):
          opti.subject_to(vertcat(1,2,3)==x[0])


    def test_value(self):
        opti = Opti()
        x = opti.variable()
        y = opti.variable()
        z = opti.variable()
        p = opti.parameter()
        q = opti.parameter()
        g = x-p>=0
        opti.subject_to(g)
        opti.minimize(x**2+(y-3)**2)
        lam = opti.dual(g)
        
        self.assertEqual(opti.debug.value(p**3,[p==2]),8)
        self.assertEqual(opti.debug.value(x**3,[x==2]),8)
        self.assertEqual(opti.debug.value(x+p,[x==2,p==3]),5)
        self.assertEqual(opti.debug.value(lam**3,[opti.lam_g==2]),8)
        with self.assertInException("This expression depends on a parameter with unset value"):
          opti.debug.value(p**3)
        with self.assertInException("This action is forbidden since you have not solved"):
          opti.debug.value(x**3)
        with self.assertInException("This action is forbidden since you have not solved"):
          opti.debug.value(lam**3)
        opti.solver("ipopt")
        
        opti.set_value(p,2)
        sol = opti.solve()
        self.assertEqual(opti.debug.value(p**2),4)
        self.assertEqual(opti.debug.value(p**2,[p==3]),9)
        self.checkarray(opti.debug.value(x**2),4,digits=5)
        self.checkarray(opti.debug.value(x**2,[x==3]),9)
        self.checkarray(opti.debug.value(lam**2),16,digits=5)
        self.checkarray(opti.debug.value(lam**2,[opti.lam_g==1]),1,digits=5)
        with self.assertInException("This expression has symbols that do not appear in the constraints and objective:"):
          opti.debug.value(z**3)
        self.assertEqual(opti.debug.value(z**3,[z==2]),8)
        with self.assertInException("This expression depends on a parameter with unset value"):
          opti.debug.value(q)

    def test_introspection(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      p = opti.parameter()
      
      opti.minimize((x-y**2)**2)
      opti.subject_to(x+y+p>=1)
      opti.subject_to(z+x>=1)
      
      opti.solver('ipopt')
      opti.set_value(p, 3)
      sol = opti.solve()

      solver = nlpsol("solver","ipopt",{"x": opti.x, "f": opti.f, "g": opti.g, "p": opti.p})
      sol2 = solver(p=sol.value(p),lbg=sol.value(opti.lbg),ubg=sol.value(opti.ubg))
      
      self.checkarray(sol2["x"],sol.value(opti.x))
      
    def test_max_iter(self):
      opti = Opti()
      x = opti.variable()
      opti.minimize((x-1)**6)
      opti.solver('ipopt',{},{"max_iter":1})
      with self.assertInException("Maximum_Iterations_Exceeded"):
        sol = opti.solve()

      sol = opti.solve_limited()
      opti.solver('ipopt',{},{"max_iter":1000})
      opti.subject_to(x>=1)
      opti.subject_to(x<=-1)

      with self.assertInException("Infeasible"):
        sol = opti.solve()

      with self.assertInException("Infeasible"):
        sol = opti.solve_limited()

    @requires_conic("superscs")
    def test_conic(self):
      options = {"eps":1e-9,"do_super_scs":1, "verbose":0}

      opti = Opti('conic')
      x = opti.variable()
      y = opti.variable()

      #  min  2 x + y
      #
      #    ||  x-5 , y-7 ||_2 <= 4
      #
      #
      for x_scale in [1,7]:
        for g_scale in [1,9]:
          opti.set_linear_scale(x,x_scale)

          h = soc(vertcat(x-5,y-7),4)

          # Note: >= destroys sparsity
          opti.subject_to(h>0,g_scale)
      
          opti.minimize(2*x+y)

          opti.solver("superscs",{},options)
          sol = opti.solve()

          res = sol.value(vertcat(x,y))

          self.checkarray(res,DM([5-8/sqrt(5),7-4/sqrt(5)]),conic,digits=7)
          self.checkarray(sol.value(opti.f),10-16/sqrt(5)+7-4/sqrt(5),conic,digits=7)
   
    @requires_conic("cbc")
    def test_discrete_linear(self):
      opti = Opti('conic')
      x = opti.variable()
      y = opti.variable()
      
      opti.minimize(x+y)
      opti.subject_to(y>=0.5*x+1)
      opti.subject_to(y<=2*x+3)
      
      #opti.subject_to(-5<= (x <= 5))
      #opti.subject_to(-5<= (y <= 5))
      #opti.subject_to(-5<= (y <= 5))
      
      opti.set_domain(x, "real")
      opti.solver("cbc")
      
      sol = opti.solve()
      
      f_real = sol.value(opti.f)
      xsol_real = sol.value(x)
      print(f_real,xsol_real)
      opti.set_domain(x, "integer")
      
      sol = opti.solve()
      
      f_integer = sol.value(opti.f)
      xsol_integer = sol.value(x)
      print(f_integer,xsol_integer)
      self.checkarray(round(xsol_integer), xsol_integer)
      self.assertTrue(f_integer> f_real)
 
    @requires_nlpsol("bonmin")
    def test_discrete(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      p = opti.parameter()
      opti.set_value(p,-1)
      
      opti.minimize(x**2+y**2)
      opti.subject_to(x+y+p>=0)
      
      opti.set_domain(x, "real")
      opti.solver("bonmin")
      
      sol = opti.solve()
      
      f_real = sol.value(opti.f)
      xsol_real = sol.value(x)
      opti.set_domain(x, "integer")
      
      sol = opti.solve()
      
      f_integer = sol.value(opti.f)
      xsol_integer = sol.value(x)
      self.checkarray(round(xsol_integer), xsol_integer)
      self.assertTrue(f_integer> f_real)
      
      f = opti.to_function('f',[p],[x])
      self.checkarray(f(-1), xsol_integer)
      
    @requires_nlpsol("ipopt")
    def test_linear_scale(self):
    
      x = MX.sym("x")
      

      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y)**2)
      opti.subject_to(x+y>=1)
      opti.subject_to(z+x>=1)
      
      opti.set_initial(x,1)
      opti.set_initial(y,2)
      opti.set_initial(z,1)
      
      opti.solver("ipopt",{"specific_options": {"nlp_f": {"final_options":{"dump_in":True,"dump_out":True}}, "nlp_grad_f": {"final_options":{"dump_out":True}},"nlp_jac_g": {"final_options":{"dump_out":True}}},"ipopt.nlp_scaling_method":"none","ipopt.mumps_permuting_scaling":0,"ipopt.mumps_scaling":0})

      sol = opti.solve()
      
      x_sol_unscaled = sol.value(opti.x)
      
      x_unscaled = DM.from_file("nlp_f.000000.in.x.mtx")
      f_unscaled = DM.from_file("nlp_f.000000.out.f.mtx")
      grad_f_unscaled = DM.from_file("nlp_grad_f.000000.out.grad_f_x.mtx")
      jac_g_unscaled = DM.from_file("nlp_jac_g.000000.out.jac_g_x.mtx")
      
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y)**2)
      opti.subject_to(x+y>=1)
      opti.subject_to(z+x>=1)
      
      opti.set_initial(x,1)
      opti.set_initial(y,2)
      opti.set_initial(z,1)
      
      opti.set_linear_scale(x,10)
      opti.set_linear_scale(y,5,1)
      opti.set_linear_scale(z,3,1)
      
      opti.solver("ipopt",{"specific_options": {"nlp_f": {"final_options":{"dump_in":True,"dump_out":True}}, "nlp_grad_f": {"final_options":{"dump_out":True}}},"ipopt.nlp_scaling_method":"none","ipopt.mumps_permuting_scaling":0,"ipopt.mumps_scaling":0})

      sol = opti.solve()
      
      x_sol_scaled = sol.value(opti.x)
      
      x_scaled = DM.from_file("nlp_f.000000.in.x.mtx")
      f_scaled = DM.from_file("nlp_f.000000.out.f.mtx")
      grad_f_scaled = DM.from_file("nlp_grad_f.000000.out.grad_f_x.mtx")
      
      self.checkarray((x_unscaled-vertcat(0,1,1))/vertcat(10,5,3),x_scaled)
      self.checkarray(f_unscaled, f_scaled)
      self.checkarray(x_sol_scaled, x_sol_unscaled)
      self.checkarray(grad_f_unscaled*vertcat(10,5,3),grad_f_scaled)

      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y)**2)
      opti.subject_to(x+y>=1, 10)
      opti.subject_to(z+x>=1, 3)
      
      opti.solver("ipopt",{"specific_options": {"nlp_f": {"final_options":{"dump_in":True,"dump_out":True}}, "nlp_jac_g": {"final_options":{"dump_out":True}}},"ipopt.nlp_scaling_method":"none","ipopt.mumps_permuting_scaling":0,"ipopt.mumps_scaling":0})

      sol = opti.solve()

      x_scaled = DM.from_file("nlp_f.000000.in.x.mtx")
      f_scaled = DM.from_file("nlp_f.000000.out.f.mtx")
      jac_g_scaled = DM.from_file("nlp_jac_g.000000.out.jac_g_x.mtx")
      self.checkarray(x_sol_scaled, x_sol_unscaled)
      
      self.checkarray(jac_g_scaled[0,:]*10, jac_g_unscaled[0,:])
      self.checkarray(jac_g_scaled[1,:]*3, jac_g_unscaled[1,:])

    @requires_nlpsol("ipopt")
    def test_linear_scale2(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y-z)**2)
      opti.subject_to(z-3 <= vertcat(x,y))
      opti.subject_to(vertcat(x,y) <= z+3)
      
      opti.set_initial(x,1)
      opti.set_initial(y,2)
      opti.set_initial(z,1)
      
      opti.solver("ipopt",{"specific_options": {"nlp_f": {"final_options":{"dump_in":True,"dump_out":True}}, "nlp_grad_f": {"final_options":{"dump_out":True}},"nlp_jac_g": {"final_options":{"dump_out":True}}},"ipopt.nlp_scaling_method":"none","ipopt.mumps_permuting_scaling":0,"ipopt.mumps_scaling":0})

      sol = opti.solve()
      
      x_sol_unscaled = sol.value(opti.x)
      
      x_unscaled = DM.from_file("nlp_f.000000.in.x.mtx")
      f_unscaled = DM.from_file("nlp_f.000000.out.f.mtx")
      grad_f_unscaled = DM.from_file("nlp_grad_f.000000.out.grad_f_x.mtx")
      jac_g_unscaled = DM.from_file("nlp_jac_g.000000.out.jac_g_x.mtx")
      

      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      
      opti.minimize((x-y-z)**2)
      opti.subject_to(z-3 <= vertcat(x,y))
      opti.subject_to(vertcat(x,y) <= z+3)
    
      opti.set_initial(x,1)
      opti.set_initial(y,2)
      opti.set_initial(z,1)

      opti.set_linear_scale(x,10)
      opti.set_linear_scale(y,5,1)
      opti.set_linear_scale(z,3,1)

      opti.solver("ipopt",{"specific_options": {"nlp_f": {"final_options":{"dump_in":True,"dump_out":True}}, "nlp_jac_g": {"final_options":{"dump_out":True}}},"ipopt.nlp_scaling_method":"none","ipopt.mumps_permuting_scaling":0,"ipopt.mumps_scaling":0})

      sol = opti.solve()
      
      x_sol_scaled = sol.value(opti.x)

      x_scaled = DM.from_file("nlp_f.000000.in.x.mtx")
      f_scaled = DM.from_file("nlp_f.000000.out.f.mtx")
      jac_g_scaled = DM.from_file("nlp_jac_g.000000.out.jac_g_x.mtx")
      
      self.checkarray(x_sol_scaled, x_sol_unscaled)
      self.checkarray(jac_g_scaled[:,0], jac_g_unscaled[:,0]*10)
      self.checkarray(jac_g_scaled[:,1], jac_g_unscaled[:,1]*5)
      self.checkarray(jac_g_scaled[:,2], jac_g_unscaled[:,2]*3)
  
    @requires_nlpsol("ipopt")
    def test_linear_scale3(self):
      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      opti.minimize((x-y-z)**2)
      opti.subject_to(z-3 <= (vertcat(x,y) <= z+3))
      
      opti.set_initial(x,1)
      opti.set_initial(y,2)
      opti.set_initial(z,1)
      
      opti.solver("ipopt",{"specific_options": {"nlp_f": {"final_options":{"dump_in":True,"dump_out":True}}, "nlp_grad_f": {"final_options":{"dump_out":True}},"nlp_jac_g": {"final_options":{"dump_out":True}}},"ipopt.nlp_scaling_method":"none","ipopt.mumps_permuting_scaling":0,"ipopt.mumps_scaling":0})

      sol = opti.solve()
      
      x_sol_unscaled = sol.value(opti.x)
      
      x_unscaled = DM.from_file("nlp_f.000000.in.x.mtx")
      f_unscaled = DM.from_file("nlp_f.000000.out.f.mtx")
      grad_f_unscaled = DM.from_file("nlp_grad_f.000000.out.grad_f_x.mtx")
      jac_g_unscaled = DM.from_file("nlp_jac_g.000000.out.jac_g_x.mtx")
      

      opti = Opti()
      x = opti.variable()
      y = opti.variable()
      z = opti.variable()
      
      
      opti.minimize((x-y-z)**2)
      opti.subject_to(z-3 <= (vertcat(x,y) <= z+3))
    
      opti.set_initial(x,1)
      opti.set_initial(y,2)
      opti.set_initial(z,1)

      opti.set_linear_scale(x,10)
      opti.set_linear_scale(y,5,1)
      opti.set_linear_scale(z,3,1)

      opti.solver("ipopt",{"specific_options": {"nlp_f": {"final_options":{"dump_in":True,"dump_out":True}}, "nlp_jac_g": {"final_options":{"dump_out":True}}},"ipopt.nlp_scaling_method":"none","ipopt.mumps_permuting_scaling":0,"ipopt.mumps_scaling":0})

      sol = opti.solve()
      
      x_sol_scaled = sol.value(opti.x)

      x_scaled = DM.from_file("nlp_f.000000.in.x.mtx")
      f_scaled = DM.from_file("nlp_f.000000.out.f.mtx")
      jac_g_scaled = DM.from_file("nlp_jac_g.000000.out.jac_g_x.mtx")
      
      self.checkarray(x_sol_scaled, x_sol_unscaled)
      self.checkarray(jac_g_scaled[:,0], jac_g_unscaled[:,0]*10)
      self.checkarray(jac_g_scaled[:,1], jac_g_unscaled[:,1]*5)
      self.checkarray(jac_g_scaled[:,2], jac_g_unscaled[:,2]*3)
      
    def test_detect_simple_bounds(self):
  
      checks = ["f","g","lbg","ubg","lam_g"]
      
      ref = {}
      for scale_x in [None,1,9]:
        for scale_g in [None,1, 100]:
          for detect_simple_bounds in [False,True]:
            opti = Opti()
            x = opti.variable()
            y = opti.variable()
            z = opti.variable()
            
            if scale_x is not None:
              opti.set_linear_scale(x,scale_x)

            opti.set_initial(x,12)
            opti.set_initial(y,12)
            opti.set_initial(z,12)

            if scale_g is None:
              opti.subject_to(-5 <= (x <= 7))
            else:
              opti.subject_to(-5 <= (x <= 7), scale_g)

            opti.subject_to(-3 <= (-y <= 2))
            opti.subject_to(-2 <= (-y <= 1))
            opti.subject_to(-3 <= (-0.3*z <= 2))
            opti.subject_to(-1 <= (-0.3*z <= 0))
            opti.subject_to(-4 <= (x <= 6))

            opti.minimize((x-10)**2+(y-10)**2+(z-10)**2)

            opti.solver("ipopt",{"detect_simple_bounds": detect_simple_bounds})

            sol = opti.solve()
            
            for k in checks:
              if scale_x is None and scale_g is None and not detect_simple_bounds:
                ref[k] = sol.value(getattr(opti,k))
              else:
                self.checkarray(ref[k], sol.value(getattr(opti,k)), digits=6)

    @memory_heavy()
    @requires_nlpsol("ipopt")
    def test_ipopt_custom_jac(self):
    
      # f_scale
      for x_scale in [vertcat(1,1,1),vertcat(7,0.11,0.13)]:
        for x_scale_offset in [vertcat(0,0,0),vertcat(1,2,3)]:
          for g_scale in [vertcat(1,1),vertcat(3,5)]:
            for f_scale in [1,1.7]:
              for scale_helper in [True,False]:
                opti = Opti()
                x=opti.variable()
                y=opti.variable()
                w=opti.variable()

                
                opti.set_linear_scale(x,x_scale[0],x_scale_offset[0])
                opti.set_linear_scale(y,x_scale[1],x_scale_offset[1])
                opti.set_linear_scale(w,x_scale[2],x_scale_offset[2])
                
                opti.minimize((1-x)**2+100*w**2,f_scale)
                opti.subject_to(y-x**2-w==0,g_scale[0])
                opti.subject_to(w**2-y==7,g_scale[1])
                
                opti.solver("ipopt")
                opti.solve()
               

                ref_solver = opti.debug.casadi_solver


                opti = Opti()
                x=opti.variable()
                y=opti.variable()
                w=opti.variable()
                
                
                opti.set_linear_scale(x,x_scale[0],x_scale_offset[0])
                opti.set_linear_scale(y,x_scale[1],x_scale_offset[1])
                opti.set_linear_scale(w,x_scale[2],x_scale_offset[2])
                
                opti.minimize((1-x)**2+100*w**2,f_scale)
                opti.subject_to(y-x**2-w==0,g_scale[0])
                opti.subject_to(w**2-y==7,g_scale[1])
                

                
                if scale_helper:
                  nlp_jac_g_custom = opti.scale_helper(Function('nlp_jac_g',[opti.x,opti.p],[opti.g,jacobian(opti.g,opti.x)],["x","p"],["g","jac_g_x"]))
                else:
                  nlp_jac_g_custom = Function('nlp_jac_g',[opti.x,opti.p],substitute([opti.g/opti.g_linear_scale,mtimes(jacobian(opti.g/opti.g_linear_scale,opti.x),diag(opti.x_linear_scale))],[opti.x],[opti.x*opti.x_linear_scale+opti.x_linear_scale_offset]),["x","p"],["g","jac_g_x"])

                options = {}
                options["cache"] = {"nlp_jac_g":nlp_jac_g_custom}
                opti.solver("ipopt", options)
                try:
                  sol = opti.solve()
                except:
                  pass
                
                solver = opti.debug.casadi_solver
                
                #print(sol.value(opti.f+dot(opti.lam_g, opti.g)))

                print(opti.x_linear_scale)
                print(opti.x_linear_scale_offset)
                print(opti.g_linear_scale)
                print(opti.f_linear_scale)
                self.checkfunction_light(ref_solver.get_function("nlp_jac_g"),solver.get_function("nlp_jac_g"),inputs=[vertcat(0.11,0.3,0.7),0])
                lam_f = MX.sym("lam_f")
                if scale_helper:
                  lag = lam_f*opti.f+dot(opti.lam_g,opti.g)
                  H = jacobian(gradient(lag,opti.x),opti.x,{"symmetric":True})
                  nlp_hess_l_custom = opti.scale_helper(Function('nlp_hess_l',[opti.x,opti.p,lam_f,opti.lam_g],[triu(H)],["x","p","lam_f","lam_g"],["triu_hess_gamma_x_x"]))
                else:
                  lag = lam_f*opti.f/f_scale+dot(opti.lam_g,opti.g/opti.g_linear_scale)
                  H = mtimes(jacobian(gradient(lag,opti.x),opti.x,{"symmetric":True}),diag(opti.x_linear_scale)**2)
                  H = substitute(triu(H),opti.x,opti.x*opti.x_linear_scale+opti.x_linear_scale_offset)
                  nlp_hess_l_custom = Function('nlp_hess_l',[opti.x,opti.p,lam_f,opti.lam_g],[H])
                  
                print(ref_solver.get_function("nlp_hess_l"))
                self.checkfunction_light(ref_solver.get_function("nlp_hess_l"),nlp_hess_l_custom,inputs=[vertcat(0.11,0.3,0.7),0,3,17])

    @memory_heavy()
    @requires_nlpsol("ipopt")
    def test_scaling(self):
    
      f_ref = None
      g_ref = None
      x_ref = None
      lam_g_ref = None
      grad_f_ref = None
      jac_g_ref = None
      
      dual_ref = None
      lbg_ref = None
      for x_scale in [1,100]:
        for g_scale in [1,37]:
          for f_scale in [1,11]:
            print(x_scale,g_scale)

            opti = Opti()
            x=opti.variable()
            y=opti.variable()
            w=opti.variable()
            
            
            opti.set_linear_scale(x,x_scale)
            
            
            opti.minimize((1-x)**2+100*(y-x**2)**2,f_scale)
            my_g = x**2+y**2==1
            opti.subject_to(my_g,g_scale)
            
            opti.solver("ipopt",{"ipopt.print_level":0,"print_time":False})
            sol = opti.solve()
            
            print(sol.value(opti.lbg))
            
            if x_scale==1 and g_scale==1 and f_scale==1:
              f_ref = sol.value(opti.f)
              g_ref = sol.value(opti.g)
              x_ref = sol.value(opti.x)
              lam_g_ref = sol.value(opti.lam_g)
              grad_f_ref = sol.value(gradient(opti.f,opti.x))
              jac_g_ref = sol.value(jacobian(opti.g,opti.x))
              dual_ref = sol.value(opti.dual(my_g))
              lbg_ref = sol.value(opti.lbg)
            else:
              self.checkarray(f_ref,sol.value(opti.f))
              self.checkarray(g_ref,sol.value(opti.g))
              self.checkarray(x_ref,sol.value(opti.x))
              self.checkarray(lam_g_ref,sol.value(opti.lam_g),digits=6)
              self.checkarray(grad_f_ref, sol.value(gradient(opti.f,opti.x)),digits=6)
              self.checkarray(jac_g_ref, sol.value(jacobian(opti.g,opti.x)),digits=6)
              self.checkarray(dual_ref, sol.value(opti.dual(my_g)),digits=6)
              self.checkarray(lbg_ref, sol.value(opti.lbg))
            
            lag_grad = sol.value(gradient(opti.f+dot(opti.lam_g, opti.g),opti.x))
            self.checkarray(sol.value(x), 0.78641515, digits=6)
            self.checkarray(lag_grad, vertcat(0,0), digits=6)

    @requires_conic("highs")
    @requires_nlpsol("ipopt")
    def test_dual(self):
    
        ref = {}
        
        for t in ['nlp','conic']:
            opti = Opti(t)
            x = opti.variable()
            y = opti.variable()
            z = opti.variable()
            opti.minimize(x**2+y**2+z**2)
            g1 = 2*x+3*y+4<=0
            opti.subject_to(g1)
            g2 = 7*x+3*z+6==0
            opti.subject_to(g2)
            opti.solver('highs' if t=='conic' else 'ipopt')
            
            sol = opti.solve()
            
            if t=='conic':
                data = {}
            else:
                data = ref
            
            data["x"] = sol.value(opti.x)
            data["lam_g"] = sol.value(opti.lam_g)
            data["g1"] = sol.value(opti.dual(g1))
            data["g2"] = sol.value(opti.dual(g2))
        print(data)
        print(ref)
        for k in data.keys():
            self.checkarray(data[k],ref[k],digits=6)
    
    @requires_conic("superscs")
    @requires_nlpsol("ipopt")
    def test_dual_soc(self):
    
        ref = {}
        
        for t in ['conic']:
            opti = Opti(t)
            x = opti.variable()
            y = opti.variable()
            z = opti.variable()
            h = soc(vertcat(x-5,y-7),4)

            # Note: >= destroys sparsity
            opti.subject_to(h>0)
            g1 = 1*x+2*y+3*z+3==0
            opti.subject_to(g1)
        
            opti.minimize(2*x+y)
            
            if t=='conic':
                opti.solver('superscs',{"superscs": {"eps":1e-9,"do_super_scs":1, "verbose":0}})
            else:
                opti.solver("ipopt")

            sol = opti.solve()
            
            if t=='conic':
                data = {}
            else:
                data = ref
            data["f"] = sol.value(opti.f)
            data["x"] = sol.value(opti.x)
            data["lam_g"] = sol.value(opti.lam_g)
            #data["g1"] = sol.value(opti.dual(g1))
            #data["g2"] = sol.value(opti.dual(g2))
            print(data)


     # to_function with lam_g
if __name__ == '__main__':
    unittest.main()
