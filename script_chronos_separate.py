"""
I created separate models for each site and backtested them using multiple time windows
The results show notable variance in estimation WAPEs: from ~0.23 (site 12, window 0) to 
~0.69 (site 6, window 0)
{
 2: {
     0: {'WAPE': np.float64(-0.4628316560864566)},
     1: {'WAPE': np.float64(-0.4018627833278402)},
     2: {'WAPE': np.float64(-0.26267797980029695)},
     3: {'WAPE': np.float64(-0.44088945800496016)},
     4: {'WAPE': np.float64(-0.3548706157304809)}
     },
 4: {
     0: {'WAPE': np.float64(-0.3001447020687129)},
     1: {'WAPE': np.float64(-0.37648481829953834)},
     2: {'WAPE': np.float64(-0.291591182448398)},
     3: {'WAPE': np.float64(-0.42956077448318203)},
     4: {'WAPE': np.float64(-0.37819249735305677)}
     },
 5: {
     0: {'WAPE': np.float64(-0.3720353373084096)},
     1: {'WAPE': np.float64(-0.4985136909847851)},
     2: {'WAPE': np.float64(-0.2932703240535373)},
     3: {'WAPE': np.float64(-0.3376355404275072)},
     4: {'WAPE': np.float64(-0.4298635695276259)}
     },
 6: {
     0: {'WAPE': np.float64(-0.6883984127707382)},
     1: {'WAPE': np.float64(-0.6345333143786852)},
     2: {'WAPE': np.float64(-0.6394294386716116)},
     3: {'WAPE': np.float64(-0.4583913714229686)},
     4: {'WAPE': np.float64(-0.6459478577273244)}
     },
 12: {
      0: {'WAPE': np.float64(-0.22741176954962097)},
      1: {'WAPE': np.float64(-0.35722274386114833)},
      2: {'WAPE': np.float64(-0.5208853094100114)},
      3: {'WAPE': np.float64(-0.45653157259658866)},
      4: {'WAPE': np.float64(-0.5028341390777316)}
      }
 }

I tried using covariates (a.k.a features/exogenous variables)
but found out later that they are not yet supported for Chronos.

"""

from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
from autogluon.timeseries.splitter import ExpandingWindowSplitter
import preprocessing_chronos

sites_ids = [2, 4, 5, 6, 12]
sites_data = preprocessing_chronos.get_chronos_compatible_sites()

prediction_length = 36
num_val_windows=5

all_wapes = {}

for site_id in sites_ids:
    
    data = TimeSeriesDataFrame.from_data_frame(sites_data.get(site_id))
    train_data, test_data = data.train_test_split(prediction_length)
    
    
    predictor = TimeSeriesPredictor(
        prediction_length=prediction_length,
        path=f'./models/separate/{site_id}',
        target='target',
        eval_metric='WAPE',
    )
    
    predictor.fit(train_data, presets="chronos_tiny")
    predictions = predictor.predict(train_data)
    
    predictor.plot(test_data, predictions, quantile_levels=[0.1, 0.9], max_history_length=100)
    
    one_site_wapes = {}
    splitter = ExpandingWindowSplitter(prediction_length=prediction_length, num_val_windows=num_val_windows)
    for window_idx, (train_split, val_split) in enumerate(splitter.split(test_data)):
        score = predictor.evaluate(val_split)
        one_site_wapes[window_idx] = score
    all_wapes[site_id] = one_site_wapes