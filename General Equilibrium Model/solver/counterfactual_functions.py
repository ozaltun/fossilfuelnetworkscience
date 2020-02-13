import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from helper import *
## These functions have had a basic "check".
def get_E_hat(w_hat, r_hat, data):
    ''' This is a function that returns the total expenditure change for all countries as a vector E_hat.
    variables: w_hat, r_hat
    parameters: data['e_L'], data['e']
    output: E_hat (nx1)
    '''
    E_hat = w_hat*data['e_L'] + (r_hat * data['e']).sum(axis=1).reshape((data['n'], 1))
    return E_hat

def get_P_k_hat(P_k_goods_hat, data):
    ''' This is a function that returns the price index change for a country as a vector P_k_hat.
    variables: P_k_goods_hat
    parameters: data['alpha'], data['sigma']
    output: P_k_hat (nx1)
    '''
    new_matrix = data['alpha'] * (P_k_goods_hat)**(1-data['sigma'])
    P_k_hat = (new_matrix.sum(axis=1))**(1/(1-data['sigma']))

    return P_k_hat

def get_P_k_goods_hat(C_k_hat, data):
    ''' This is a function that returns the price index for final goods change for a country and final good matrix.
    variables: C_k_hat
    parameters: data['lambda_k'], data['theta_k']
    output: P_k_goods_hat (nxk)
    '''

    C_k_hat_temp = C_k_hat ** (-data['theta_k'].reshape((1, data['k'])))
    part1 = np.sum(data['lambda_k'] * C_k_hat_temp.reshape((1, data['n'], data['k'])), axis=1)
    part2 = part1.reshape((data['n'], data['k']))
    P_k_goods_hat = part2 ** (-1/data['theta_k'].reshape((1, data['k'])))

    return P_k_goods_hat

def get_P_g_goods_hat(C_g_hat, data):
    ''' This is a function that returns the price index for change inn commodities for a country and commodity matrix.
    variables: C_g_hat
    parameters: data['lambda_g'], data['theta_g']
    output: P_g_goods_hat (nxg)
    '''

    C_g_hat_temp = C_g_hat ** (-data['theta_g'].reshape((1, data['g'])))
    part1 = np.sum(data['lambda_g'] * C_g_hat_temp.reshape((1, data['n'], data['g'])), axis=1)
    part2 = part1.reshape((data['n'], data['g']))
    P_g_goods_hat = part2 ** (-1/data['theta_g'].reshape((1, data['g'])))

    return P_g_goods_hat

def get_D_k_hat(E_hat, P_k_goods_hat, P_k_hat, data):
    ''' This is a function that returns the demand for final goods for a country.
    variables: E_hat, P_k_goods_hat, P_k_hat
    parameters: data['sigma']
    output: D_k_hat (nxk)'''

    D_k_hat = E_hat.reshape((data['n'], 1)) * ((P_k_goods_hat/P_k_hat.reshape((data['n'], 1))) ** (1 - data['sigma']))

    return D_k_hat

def get_D_g_hat(P_g_goods_hat, C_k_hat, Y_k_hat, data):
    ''' This is a function that returns the demand for commodities for a country.
    variables: P_g_goods_hat, C_k_hat, Y_k_hat
    parameters: data['d'], data['eta']
    output: D_c_hat (nxg)

    TODO: Problem with reshape

    '''
    part1 = (P_g_goods_hat.reshape((data['n'], 1, data['g']))/C_k_hat.reshape((data['n'], data['k'], 1)) ) ** (1 - data['eta'].reshape(1, data['k'], 1))
    part2 = data['d'] * part1 * Y_k_hat.reshape((data['n'], data['k'], 1))

    D_g_hat = part2.sum(axis=1).reshape((data['n'], data['g']))

    return D_g_hat

def get_Y_k_hat(C_k_hat, P_k_goods_hat, D_k_hat, data):
    ''' This is a function that returns the total production for a given final good and country.
    variables: C_k_hat, P_k_hat, D_k_hat
    parameters: data['X_k'], data['Y_k'], data['theta_k']
    output: Y_k_hat (nxk)'''

    C_k_hat_temp = C_k_hat **(-data['theta_k'].reshape((1, data['k'])))
    P_k_goods_hat_temp = P_k_goods_hat **(data['theta_k'].reshape((1, data['k'])))

    part_1 = data['X_k']/data['Y_k'].reshape((1, data['n'], data['k'])) * (P_k_goods_hat_temp * D_k_hat).reshape((data['n'],1,data['k']))

    Y_k_hat = (C_k_hat_temp.reshape((1, data['n'], data['k']))*part_1).sum(axis=0).reshape(data['n'], data['k'])

    return Y_k_hat

def get_Y_g_hat(C_g_hat, P_g_goods_hat, D_g_hat, data):
    ''' This is a function that returns the total production for a given final good and country.
    variables: C_g_hat, P_g_goods_hat, D_g_hat
    parameters: data['X_g'], data['Y_g'], data['theta_g']
    output: Y_g_hat (nxg)'''

    C_g_hat_temp = C_g_hat **(-data['theta_g'].reshape((1, data['g'])))
    P_g_goods_hat_temp = P_g_goods_hat **(data['theta_g'].reshape((1, data['g'])))

    part_1 = data['X_g']/data['Y_g'].reshape((1, data['n'], data['g'])) * (P_g_goods_hat_temp * D_g_hat).reshape((data['n'],1,data['g']))

    Y_g_hat = (C_g_hat_temp.reshape((1, data['n'], data['g']))*part_1).sum(axis=0).reshape(data['n'], data['g'])

    return Y_g_hat

def get_C_k_hat(w_hat, P_g_goods_hat, data):
    ''' This is a function that returns the cost of final good in a country.
    variables: w_hat, P_g_goods_hat
    parameters: data['phi_L_k'], data['phi'], data['eta']
    output: C_k_hat (nxk)'''

    part1 = data['phi_L_k'] * (w_hat.reshape((data['n'], 1)) ** (1 - data['eta'].reshape((1, data['k']))))
    part2 = data['phi'] * ((P_g_goods_hat.reshape(data['n'], 1, data['g'])) ** (1 - data['eta'].reshape((1, data['k'],1))) )

    C_k_hat = (part1 + np.sum(part2, axis=2).reshape((data['n'], data['k']))) ** (1/(1-data['eta'].reshape((1, data['k'])) ))

    return C_k_hat

def get_C_g_hat(w_hat, r_hat, data):
    ''' This is a function that returns the cost of Commodities in a country.
    variables: w_hat, r_hat
    parameters: data['phi_L_g'], data['phi_R'], data['rho_g']
    output: C_G_hat (nxg)
    '''
    print(r_hat[r_hat<0])
    part1 = data['phi_R'] * (r_hat ** (1- data['rho_g'].reshape((1, data['g']))))
    part2 = data['phi_L_g'] * (w_hat.reshape((data['n'], 1)) ** (1 - data['rho_g'].reshape((1, data['g']))) )

    C_g_hat = (part1 + part2) ** (1/(1-data['rho_g'].reshape((1, data['g'])) ))

    return C_g_hat

def get_r_hat(r_hat, Y_g_hat, C_g_hat, data):
    ''' This is a function that returns the ...
    variables: Y_g_hat, C_g_hat
    parameters: data['R_hat'], data['rho_g']
    output: r_hat (nxg)'''

    right_hand_side = ((r_hat/C_g_hat) ** ( 1- data['rho_g'].reshape((1, data['g'])))) * Y_g_hat

    return right_hand_side


def get_w_hat(w_hat, Y_g_hat, Y_k_hat, C_k_hat, C_g_hat, data):
    part1_part1 = data['phi_L_g']*data['Y_g']/(data['E']*data['e_L']).reshape((data['n'], 1))
    part1_part2 = ((w_hat.reshape((data['n'], 1))/C_g_hat)**(1-data['rho_g'].reshape((1, data['g'])))) *Y_g_hat

    part1 = (part1_part1*part1_part2).sum(axis=1).reshape((data['n'], 1))

    part2_part1 = data['phi_L_k']*data['Y_k']/(data['E']*data['e_L']).reshape((data['n'], 1))

    part2_part2 = ((w_hat.reshape((data['n'], 1))/C_k_hat)**(1-data['eta'].reshape((1, data['k'])))) *Y_k_hat

    part2 = (part2_part1*part2_part2).sum(axis=1).reshape((data['n'], 1))

    w_hat_new = (part1 + part2).reshape((data['n'], 1))
    return w_hat_new


def counterfactual(X, data):
    n = data['n']
    g = data['g']
    k = data['k']
    E_hat, P_k_hat, P_k_goods_hat, P_g_goods_hat, D_k_hat, D_g_hat, Y_k_hat, Y_g_hat, C_k_hat, C_g_hat, r_hat, w_hat  = get_values_from_X(X, data)

    values = []

    values.append(E_hat - get_E_hat(w_hat, r_hat, data))
    values.append(P_k_hat - get_P_k_hat(P_k_goods_hat, data))
    values.append(P_k_goods_hat - get_P_k_goods_hat(C_k_hat, data))
    values.append(P_g_goods_hat - get_P_g_goods_hat(C_g_hat, data))
    values.append(D_k_hat - get_D_k_hat(E_hat, P_k_goods_hat, P_k_hat, data))
    values.append(D_g_hat - get_D_g_hat(P_g_goods_hat, C_k_hat, Y_k_hat, data))
    values.append(Y_k_hat - get_Y_k_hat(C_k_hat, P_k_hat, D_k_hat, data))
    values.append(Y_g_hat - get_Y_g_hat(C_g_hat, P_g_goods_hat, D_g_hat, data))
    values.append(C_k_hat - get_C_k_hat(w_hat, P_g_goods_hat, data))
    values.append(C_g_hat - get_C_g_hat(w_hat, r_hat, data))
    values.append(r_hat - get_r_hat(r_hat, Y_g_hat, C_g_hat, data))
    values.append(w_hat - get_w_hat(w_hat, Y_g_hat, Y_k_hat, C_k_hat, C_g_hat, data))

    X_new = get_X_from_values(values, data)

    return X_new

def reduced_counterfactual(X, data):

    n = data['n']
    g = data['g']
    k = data['k']

    r_hat, w_hat = get_values_from_X_reduced(X, data)
    # print(r_hat.mean())

    C_g_hat = get_C_g_hat(w_hat, r_hat, data)
    E_hat = get_E_hat(w_hat, r_hat, data)

    P_g_goods_hat = get_P_g_goods_hat(C_g_hat, data)

    C_k_hat = get_C_k_hat(w_hat, P_g_goods_hat, data)

    P_k_goods_hat = get_P_k_goods_hat(C_k_hat, data)

    P_k_hat = get_P_k_hat(P_k_goods_hat, data)

    D_k_hat = get_D_k_hat(E_hat, P_k_goods_hat, P_k_hat, data)

    Y_k_hat = get_Y_k_hat(C_k_hat, P_k_goods_hat, D_k_hat, data)
    # print(np.mean(Y_k_hat))
    D_g_hat = get_D_g_hat(P_g_goods_hat, C_k_hat, Y_k_hat, data)
    # print(np.mean(D_g_hat))
    Y_g_hat = get_Y_g_hat(C_g_hat, P_g_goods_hat, D_g_hat, data)
    # print(np.mean(Y_g_hat))
    values = []
    values.append(r_hat - get_r_hat(r_hat, Y_g_hat, C_g_hat, data))
    values.append(w_hat - get_w_hat(w_hat, Y_g_hat, Y_k_hat, C_k_hat, C_g_hat, data))
    # print(get_r_hat(r_hat, Y_g_hat, C_g_hat, data)[0:3,0:3])


    output = get_Res_from_values_reduced(values, data)
    # print(output.shape)
    # print(np.mean(output))

    return output
