"""

The first valid experiment conducted.

I used site 2's data. I tried using covariates (a.k.a features/exogenous variables)
but found out later that they are not yet supported for Chronos.

{'WAPE': -0.3548706157304809}

"""

from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
import preprocessing_chronos

# sites' ids 2 4 5 6 12
sites_data = preprocessing_chronos.get_chronos_compatible_sites()

prediction_length = 36

# site 2

data = TimeSeriesDataFrame.from_data_frame(sites_data.get(2))
train_data, test_data = data.train_test_split(prediction_length)


predictor = TimeSeriesPredictor(
    prediction_length=prediction_length,
    path='./models/chronos_2',
    target='target',
    eval_metric='WAPE',
)

predictor.fit(train_data, presets="chronos_tiny")
predictions = predictor.predict(train_data)

predictor.plot(test_data, predictions, quantile_levels=[0.1, 0.9], max_history_length=100)

wape = predictor.evaluate(test_data)