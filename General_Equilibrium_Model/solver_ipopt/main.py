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

    if flag:
        temp = np.ones((X.shape[0], X.shape[0]))
        rows, cols = np.nonzero(temp)
        #rows = np.linspace(0, len(X) -1, len(X)).astype(int)
        #cols = np.linspace(0, len(X) -1, len(X)).astype(int)
        return (rows, cols)
    else:

        return jac_g(X)

root, data_dict, reg_2_num, comm_2_num = get_data_files()

n = data_dict['n']
g = data_dict['g']
k = data_dict['k']

data_dict['R_hat'] = np.ones((n, g))
data_dict['R_hat'][reg_2_num['usa'], 15] = 2
data_dict['R_hat'][reg_2_num['usa'], 16] = 2


X_0 = np.ones(n*g + n)*1.0

eval_g = lambda x: reduced_counterfactual(x, data_dict)
eval_f = lambda x: np.linalg.norm(reduced_counterfactual(x, data_dict))

nvar = X_0.shape[0]
x_L = np.zeros((nvar))
x_U = np.ones((nvar)) * 10000.0

ncon = nvar

g_L = np.zeros((nvar))*1.0
g_U = np.zeros((nvar))*1.0

eval_grad_f = grad(eval_f)
jac_g = jacobian(eval_g)
def main():
    nnzj = nvar*nvar
    nnzh =  int((nvar*(nvar+1))/2)

    nlp = pyipopt.create(nvar, x_L, x_U, ncon, g_L, g_U, nnzj, nnzh, eval_f, eval_grad_f, eval_g, eval_jac_g)

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
