"""
I created separate models for each site and backtested them using multiple time windows
The results show notable variance in estimation WAPEs: from ~0.23 (site 12, window 0) to 
~0.69 (site 6, window 0)

WAPEs with chronos_tiny
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

WAPEs with chronos_mini
{
 2: {
     0: {'WAPE': -0.39485211327630276}, 
     1: {'WAPE': -0.3593843067884765}, 
     2: {'WAPE': -0.26267977697731715}, 
     3: {'WAPE': -0.41554697243082234}, 
     4: {'WAPE': -0.3487389683801465}
     }, 
 4: {
     0: {'WAPE': -0.22793120433365574}, 
     1: {'WAPE': -0.36581420374790774}, 
     2: {'WAPE': -0.2763004893888049}, 
     3: {'WAPE': -0.4070776455831521}, 
     4: {'WAPE': -0.3428553626714468}
     }, 
 5: {
     0: {'WAPE': -0.3505179903685374}, 
     1: {'WAPE': -0.5457038982906093}, 
     2: {'WAPE': -0.22357590798978774}, 
     3: {'WAPE': -0.39777968336790737}, 
     4: {'WAPE': -0.36318221248277693}
     }, 
 6: {
     0: {'WAPE': -0.6775921167347463}, 
     1: {'WAPE': -0.6328198539666542}, 
     2: {'WAPE': -0.6284492466066144}, 
     3: {'WAPE': -0.4595557864135366}, 
     4: {'WAPE': -0.6278947014162803}
     }, 
 12: {
      0: {'WAPE': -0.15606781560304633}, 
      1: {'WAPE': -0.34543980842175837}, 
      2: {'WAPE': -0.5386716810789659}, 
      3: {'WAPE': -0.4072431714112839}, 
      4: {'WAPE': -0.5040945808761603}
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
    
    predictor.fit(train_data, presets="chronos_mini")
    predictions = predictor.predict(train_data)
    
    predictor.plot(test_data, predictions, quantile_levels=[0.1, 0.9], max_history_length=100)
    
    one_site_wapes = {}
    splitter = ExpandingWindowSplitter(prediction_length=prediction_length, num_val_windows=num_val_windows)
    for window_idx, (train_split, val_split) in enumerate(splitter.split(test_data)):
        score = predictor.evaluate(val_split)
        one_site_wapes[window_idx] = score
    all_wapes[site_id] = one_site_wapes