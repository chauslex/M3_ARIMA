# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import json
from time import time
import pickle

# <codecell>


def mean_absolute_percentage_error(y_true, y_pred):
    """
    Use of this metric is not recommended; for
  illustration only.See other regression metrics on sklearn docs
      : http
        :  // scikit-learn.org/stable/modules/classes.html#regression-metrics

           Use like any other metric >>>
      y_true = [ 3, -0.5, 2, 7 ]; y_pred = [2.5, -0.3, 2, 8]
    >>> mean_absolute_percentage_error(y_true, y_pred)
    Out[]: 24.791666666666668
    """
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# <codecell>


def parse_line(line, n_predictions):
    line = line.split(',')
    n_samples = int(line[1])
    start_idx = 6
    end_idx = n_samples + start_idx
    test_idx = end_idx - n_predictions
    train_dat = np.array(line[start_idx:test_idx]).astype(np.float)
    test_dat = np.array(line[test_idx: end_idx]).astype(np.float)

    return train_dat, test_dat

# <codecell>


def arima_predict(train_dat, n_predictions, p=2, d=0, q=0, params=None):
    arima = ARIMA(np.array(train_dat).astype(np.float), [p, d, q])
    diffed_logged_results = arima.fit(
        trend='c',
        disp=False,
        start_params=params,
        maxiter=2000)
    preds = diffed_logged_results.predict(len(train_dat),
                                          len(train_dat) + n_predictions - 1,
                                          exog=None, dynamic=False)
    if not len(preds):
        print 'Error, no predictions generated'
    return preds, diffed_logged_results.params

# <codecell>


def score_period(period, pred_values, true_values):
    delay_scores = []
    # score for each prediction step into the future (ie, 1, 2, 3..)
    for jj in range(pred_values.shape[1]):
        mape = mean_absolute_percentage_error(
            true_values[
                :, jj], pred_values[
                :, jj])
        delay_scores.append(mape)
        print 'Delay {:2.0f}\t MAPE: {:.2f}'.format(jj, mape)
    return delay_scores

# <codecell>

model_params = {'p': 1, 'd': 0, 'q': 0}

periods = {'Month': {'n_predictions': 18,
                     'pred_values': [],
                     'true_values': [],
                     'model_params': model_params},
           'Year': {'n_predictions': 6,
                    'pred_values': [],
                    'true_values': [],
                    'model_params': model_params},
           'Quart': {'n_predictions': 8,
                     'pred_values': [],
                     'true_values': [],
                     'model_params': model_params},
           'Other': {'n_predictions': 8,
                     'pred_values': [],
                     'true_values': [],
                     'model_params': model_params}}

# run training for each period
for period in periods.keys():
    fname = '{}_M3C.csv'.format(period)
    p, d, q = [periods[period]['model_params'][k] for k in ['p', 'd', 'q']]
    print 'Running {}'.format(period)
    with open(fname, 'r') as f:
        print 'doing ', fname
        params = None

        start_dt = time()
        for i, l in enumerate(f):
            if i == 0:
                continue
            elif i % 100 == 0:
                print '{:4.0f} predictions in {:4.0f} seconds'.format(i, time() - start_dt)

            train_dat, test_dat = parse_line(
                l, periods[period]['n_predictions'])
            periods[period]['true_values'].append(test_dat)

            preds, params = arima_predict(
                train_dat,
                periods[period]['n_predictions'],
                p,
                d,
                q, params=params)
            periods[period]['pred_values'].append(preds)

        periods[period]['pred_values'] = np.array(
            periods[period]['pred_values'])
        periods[period]['true_values'] = np.array(
            periods[period]['true_values'])
        scores = score_period(
            period,
            periods[period]['true_values'],
            periods[period]['pred_values'])
        periods[period]['scores'] = scores
    print 'Finished running {}'.format(period)

with open('results.pkl', 'wb') as f:
    print 'Writing results to results.pkl'
    pickle.dump(periods, f)

# <codecell>
