# import libraries
import numpy as np
import pandas as pd
from sklearn import preprocessing

from model.trmf import trmf

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def normalized_deviation(prediction, Y):
    return abs(prediction - Y).sum() / abs(Y).sum()

def apply_trmf_model(data_clv):
    data_clv['InvoiceDate'] = pd.to_datetime(data_clv['InvoiceDate'])
    data_clv['TotalSales'] = data_clv['Quantity'] * data_clv['UnitPrice']
    df = data_clv.resample('H', on='InvoiceDate').TotalSales.sum()

    new_df = pd.DataFrame(zip(flatten_list(df.index),flatten_list(df.values))); new_df.head()
    new_df.rename(columns = {0:'time', 1:'sales'}, inplace = True)

    #new_df['sales'].plot()

    sales = np.array(new_df['sales'])

    clv = preprocessing.normalize(np.array([sales,] * 370, dtype=np.float64))

    N = 370
    T = 8957
    T_train = 350
    T_test = 20
    K = 4
    lags = [1, 12, 24]
    L = len(lags)
    sigma_w = 0.5
    sigma_x = 0.1
    sigma_t = 0.0

    train = clv[:T_train, :]
    test = clv[T_train:, :]

    lambda_f = 1.
    lambda_x = 1.
    lambda_w = 1.
    lags = [1, 12, 24]
    eta = 1.
    step = 0.0001
    alpha = 1000.

    model = trmf(lags, K, lambda_f, lambda_x, lambda_w, alpha, eta)
    model.fit(train)
    train_preds = np.dot(model.F, model.X)
    #nd = normalized_deviation(train_preds, train)

    # # TRMF model
    # lambda_f = 1.
    # lambda_x = 1.
    # lambda_w = 1.
    # eta = 1.
    # alpha = 1000.
    # max_iter = 1000

    # for h in [1, 5, 10, 20]:
    #     model = trmf(lags, K, lambda_f, lambda_x, lambda_w, alpha, eta, max_iter)
    #     scores_nd = RollingCV(model, clv, T-9-h, h, T_step=1, metric='ND')
    #     scores_nrmse = RollingCV(model, clv, T-9-h, h, T_step=1, metric='NRMSE')
    #     print('TRMF performance ND/NRMSE (h = {}): {}/{}'.format(h, round(np.array(scores_nd).mean(),3),\
    #                                                     round(np.array(scores_nrmse).mean(),3)))
    return new_df['sales'], clv, train_preds