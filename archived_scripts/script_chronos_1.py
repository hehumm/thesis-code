"""
site 2 data only

First try at implementing Chronos. I misunderstood the user guide and converted the exogenous
variables into independent equally-important time series (as load_energy_sum) as a result.

This led to AutoGluon finding one model that would predict values for all of the different
time series the most accurately overall.

Even here I managed to get 
{'WAPE': -0.357790652712122}
which is about as good as the current prediction method but using Chronos is much simpler

"""

from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
import preprocessing_general

# sites' ids 2 4 5 6 12
long_data = preprocessing_general.get_sites_with_data_long()

prediction_length = 36

modified_df = long_data.get(2)
modified_df['timestamp'] = modified_df['timestamp'].dt.tz_localize(None)
data = TimeSeriesDataFrame.from_data_frame(modified_df)
train_data, test_data = data.train_test_split(prediction_length)


predictor = TimeSeriesPredictor(
    prediction_length=prediction_length,
    path='./models/chronos_1',
    target='target',
    eval_metric='WAPE',
)

predictor.fit(train_data, presets="chronos_tiny")
predictions = predictor.predict(train_data)

predictor.plot(test_data, predictions, quantile_levels=[0.1, 0.9], max_history_length=100)

wape = predictor.evaluate(test_data, model=predictor.model_best())
print(wape)