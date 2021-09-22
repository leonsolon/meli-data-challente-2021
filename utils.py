import json

import numpy as np
import tweedie


def pred_list_to_prob_array(pred_list, cumulative=False, total_days=30):
    prob_array = np.zeros((pred_list.shape[0], total_days))
    pred_list = np.clip(pred_list, 1, total_days)
    for row, e in enumerate(pred_list):
        if cumulative:
            prob_array[row, int(e - 1)] = 1.
        else:
            prob_array[row, int(e - 1):] = 1.

    if cumulative:
        prob_array = prob_array + 1e-4
        prob_array = np.divide(prob_array, prob_array.sum(axis=1).reshape(-1, 1))
        prob_array = prob_array.cumsum(axis=1)

    return prob_array


def rps(y, p, probs=False, total_days=30):
    y_array = pred_list_to_prob_array(y, total_days=total_days)
    if probs:
        p_array = p.cumsum(axis=1)
    else:
        p_array = pred_list_to_prob_array(p, cumulative=True, total_days=total_days)
    return ((p_array - y_array) ** 2).sum(axis=1).mean()


def pred_list_to_tweedie(pred_list, phi=1, p=1.5):
    distros = dict()
    for mu in range(1, 31):
        distros[mu] = [tweedie.tweedie(p=p, mu=mu, phi=phi).cdf(days) for days in range(1, 31, 1)]
        distros[mu][1:] = np.diff(distros[mu])
        distros[mu] = np.round(distros[mu] / np.sum(distros[mu]), 4)

    prob_array = np.zeros((pred_list.shape[0], 30))

    for row, mu in enumerate(pred_list):
        prob_array[row, :] = distros[mu]

    return prob_array


def json_to_list(file_name):
    resultado = []

    with open(file_name, 'rb') as arquivo_treino:
        for linha in arquivo_treino:
            resultado.append(json.loads(linha))

    return resultado
