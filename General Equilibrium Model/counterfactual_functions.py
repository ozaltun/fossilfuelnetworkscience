import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## These functions have had a basic "check".
def get_E_hat(w_hat, r_hat, data):
    ''' This is a function that returns the total expenditure change for all countries as a vector E_hat.
    variables: w_hat, r_hat
    parameters: data['e_L'], data['e_R']
    output: E_hat (nx1)
    '''
    E_hat = w_hat*data['e_L'] + (r_hat * data['e_R']) @ np.ones((data['g'], 1))
    return E_hat


def get_P_f_hat(P_f_goods_hat, data):
    ''' This is a function that returns the price index change for a country as a vector P_f_hat.
    variables: P_f_goods_hat
    parameters: data['alpha'], data['sigma']
    output: P_f_hat (nx1)
    '''
    new_matrix = data['alpha'] * (P_f_goods_hat)**(1-data['sigma'])
    P_f_hat = (new_matrix @ np.ones((data['k'], 1)) )**(1/(1-data['sigma']))

    return P_f_hat

def get_P_f_goods_hat(C_f_hat, data):
    ''' This is a function that returns the price index for final goods change for a country and final good matrix.
    variables: C_f_hat
    parameters: data['lambda_f'], data['theta_k']
    output: P_f_goods_hat (nxk)
    '''

    P_f_goods_hat = np.zeros((data['n'], data['k']))
    C_f_hat_temp = C_f_hat ** (-data['theta_k'].reshape((1, data['k'])))
    part1 = np.sum(data['lambda_f'] * C_f_hat_temp.reshape((1, data['n'], data['k'])), axis=1)
    part2 = part1.reshape((data['n'], data['k']))
    P_f_goods_hat = part2 ** (-1/data['theta_k'].reshape((1, data['k'])))

    return P_f_goods_hat

def get_P_c_goods_hat(C_g_hat, data):
    ''' This is a function that returns the price index for change inn commodities for a country and commodity matrix.
    variables: C_g_hat
    parameters: data['lambda_c'], data['theta_g']
    output: P_g_goods_hat (nxg)
    '''

    P_g_goods_hat = np.zeros((data['n'], data['g']))
    C_g_hat_temp = C_g_hat ** (-data['theta_g'].reshape((1, data['g'])))
    part1 = np.sum(data['lambda_c'] * C_g_hat_temp.reshape((1, data['n'], data['g'])), axis=1)
    part2 = part1.reshape((data['n'], data['g']))
    P_g_goods_hat = part2 ** (-1/data['theta_g'].reshape((1, data['g'])))

    return P_g_goods_hat
