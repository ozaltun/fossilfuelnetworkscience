import autograd.numpy as np
import pyipopt
from autograd import grad, hessian, jacobian

import matplotlib.pyplot as plt
from counterfactual_functions import *
from helper import *


def get_data_files():
    print('Need to input path to data!')
    root = input('Please input root path')

    data_dict = load_obj(root+'/data_20200219.pickle')
    reg_2_num = load_obj(root+'/reg_2_num.pickle')
    comm_2_num = load_obj(root+'/comm_2_num.pickle')

    return root, data_dict, reg_2_num, comm_2_num

def eval_jac_g(X, flag, user_data=None):
    """
    Evaluate the sparse Jacobian of constraint functions g.
    @param X: parameter values
    @param flag: this asks for the sparsity structure
    """
    print('eval_jac_g')
    print(X)
    print(flag)
    print(user_data)
    print()
    #XXX
    if flag:
        rows = np.array([], dtype=int)
        cols = np.array([], dtype=int)
        return (rows, cols)
    else:
        return np.array([], dtype=float)

root, data_dict, reg_2_num, comm_2_num = get_data_files()

n = data_dict['n']
g = data_dict['g']
k = data_dict['k']

data_dict['R_hat'] = np.ones((n, g))
data_dict['R_hat'][reg_2_num['usa'], 15] = 2
data_dict['R_hat'][reg_2_num['usa'], 16] = 2

X_0 = np.ones(n*g + n)*1.0

def eval_g(X, user_data=None):
    """
    Evaluate the constraint functions.
    """
    return np.array([], dtype=float)

eeval_f = lambda x: np.sum(reduced_counterfactual(x, data_dict)**2) # Norm of residuals

nvar = X_0.shape[0]
x_L = np.zeros((nvar))
x_U = np.ones((nvar)) * 10000.0

ncon = 0

g_L = np.array([], dtype=float)
g_U = np.array([], dtype=float)

eval_grad_f = grad(eval_f)

def apply_new(x):
    return True

def main():
    nnzj = 0
    nnzh = int((nvar*(nvar+1))/2)

    nlp = pyipopt.create(
            nvar,
            x_L,
            x_U,
            ncon,
            g_L,
            g_U,
            nnzj,
            nnzh,
            eval_f,
            eval_grad_f,
            eval_g,
            eval_jac_g)

    nlp.num_option('tol', 1e-5)

    print("Going to call solve")
    print("x0 = {}".format(X_0))
    x, zl, zu, constraint_multipliers, obj, status = nlp.solve(X_0)

    print('x:', x)
    print('zl:', zl)
    print('zu:', zu)
    print('constraint_multipliers:', constraint_multipliers)
    print('obj:', obj)
    print('status:', status)

    save_obj(x, root+'/x_output.pickle')

main()
