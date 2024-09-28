"""

I used a unified dataframe to try to get a generalized model that would work for all sites
Contrary to my expectations, the model performed significantly worse

WAPEs of multiple windows

{0: {'WAPE': np.float64(-0.4720393736312055)},
 1: {'WAPE': np.float64(-0.4671563283903994)},
 2: {'WAPE': np.float64(-0.4613088784938541)},
 3: {'WAPE': np.float64(-0.4417443539994012)},
 4: {'WAPE': np.float64(-0.4927156612637361)}}

"""

from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
from autogluon.timeseries.splitter import ExpandingWindowSplitter
import preprocessing_chronos

combined_sites_data = preprocessing_chronos.get_chronos_compatible_unified_df()

prediction_length = 36

data = TimeSeriesDataFrame.from_data_frame(combined_sites_data)
train_data, test_data = data.train_test_split(prediction_length)


predictor = TimeSeriesPredictor(
    prediction_length=prediction_length,
    path='./models/unified',
    target='target',
    eval_metric='WAPE',
)

predictor.fit(train_data, presets="chronos_tiny")
predictions = predictor.predict(train_data)

predictor.plot(test_data, predictions, quantile_levels=[0.1, 0.9], max_history_length=100)

wapes = {}
splitter = ExpandingWindowSplitter(prediction_length=prediction_length, num_val_windows=5)
for window_idx, (train_split, val_split) in enumerate(splitter.split(test_data)):
    score = predictor.evaluate(val_split)
    wapes[window_idx] = score