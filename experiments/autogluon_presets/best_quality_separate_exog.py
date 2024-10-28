from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
from autogluon.timeseries.splitter import ExpandingWindowSplitter
import experiments.chronos.preprocessing_autogluon as preprocessing_autogluon

sites_ids = [2, 4, 5, 6, 12]
sites_data = preprocessing_autogluon.get_autogluon_compatible_sites_independent_dfs()

prediction_length = 36
num_val_windows=5

for site_id in sites_ids:
    data = TimeSeriesDataFrame.from_data_frame(sites_data.get(site_id))
    train_data, test_data = data.train_test_split(prediction_length)

    predictor = TimeSeriesPredictor(
        prediction_length=prediction_length,
        path=f'./models/separate_exog/{site_id}',
        target='target',
        eval_metric='WAPE',
    )

    predictor.fit(train_data, presets="fast_training", time_limit=600) # don't forget to change the preset to best_quality
    predictions = predictor.predict(train_data)
    predictions.to_csv(f'./predictions/{site_id}_separate_exog.csv')

