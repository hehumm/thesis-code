"""

I used a unified dataframe to try to get a generalized model that would work for all sites
Contrary to my expectations, the model performed significantly worse

{'WAPE': np.float64(-0.4927156612637361)}

"""

from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
import preprocessing_chronos

combined_sites_data = preprocessing_chronos.get_chronos_compatible_unified_df()

prediction_length = 36

data = TimeSeriesDataFrame.from_data_frame(combined_sites_data)
train_data, test_data = data.train_test_split(prediction_length)


predictor = TimeSeriesPredictor(
    prediction_length=prediction_length,
    path='./models/chronos_3',
    target='target',
    eval_metric='WAPE',
)

predictor.fit(train_data, presets="chronos_tiny")
predictions = predictor.predict(train_data)

predictor.plot(test_data, predictions, quantile_levels=[0.1, 0.9], max_history_length=100)

wape = predictor.evaluate(test_data)