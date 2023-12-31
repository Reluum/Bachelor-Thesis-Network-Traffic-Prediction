import numpy as np
from scipy.stats import stats
from sklearn.preprocessing import StandardScaler


def RSE(pred, true):
    return np.sqrt(np.sum((true - pred) ** 2)) / np.sqrt(np.sum((true - true.mean()) ** 2))


def CORR(pred, true):
    u = ((true - true.mean(0)) * (pred - pred.mean(0))).sum(0)
    d = np.sqrt(((true - true.mean(0)) ** 2).sum(0) * ((pred - pred.mean(0)) ** 2).sum(0))
    return (u / d).mean(-1)


def MAE(pred, true):
    return np.mean(np.abs(pred - true))


def MSE(pred, true):
    return np.mean((pred - true) ** 2)


def RMSE(pred, true):
    return np.sqrt(MSE(pred, true))


def MAPE(pred, true):
    return np.mean(np.abs((pred - true) / true))


def MSPE(pred, true):
    return np.mean(np.square((pred - true) / true))


def HVI(pred, true, interval=10):
    error = []
    for i in list(range(len(pred))):
        pred_peak_index = pred[i].argmax()
        pred_peak_value = pred[i, pred_peak_index]

        true_peak_index = true[i,
                          max(pred_peak_index - interval, 0): min(pred_peak_index + interval, true.shape[1])].argmax()
        true_peak_value = true[i, true_peak_index]

        true_actual_peak_index = true[i].argmax()
        true_actual_peak_value = true[i, true_actual_peak_index]

        error.append((pred_peak_value - true_peak_value) / true_actual_peak_value)

    return np.array(error).mean()


def pearson(context, pred, true):  # context = [B,L,1]; pred = true = [B,P,1]
    residual = (pred - true).squeeze(axis=-1)
    context = context.squeeze(axis=-1)
    true = true.squeeze(axis=-1)
    pred = pred.squeeze(axis=-1)
    prs = 0
    pts = 0

    for i in range(context.shape[1]):
        c = context[:, i]
        for j in range(residual.shape[1]):
            cr, pr = stats.pearsonr(c, residual[:, j])
            ct, pt = stats.pearsonr(c, true[:, j])

            if pr < 0.01 and pt < 0.01:
                prs += cr
                pts += ct

        print(f"[x] Processing pearson: {i / context.shape[1]}")

    return prs, pts


def metric(pred, true):
    mae = MAE(pred, true)
    mse = MSE(pred, true)
    rmse = RMSE(pred, true)
    mape = MAPE(pred, true)
    mspe = MSPE(pred, true)
    hvi = HVI(pred, true)

    return mae, mse, rmse, mape, mspe, hvi
