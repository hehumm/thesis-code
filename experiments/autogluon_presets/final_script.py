import os

import experiments.autogluon_presets.model_training as model_training
import experiments.chronos.preprocessing_autogluon as preprocessing_autogluon

#common_path='/home/henri/Code/thesis-code/experiments/autogluon_presets'
common_path='/root/code/thesis-code/experiments/autogluon_presets'

# possible metrics: 'MAE', 'WAPE', 'MSE', 'RMSE'
def train_for_one_metric(metric):
    sites_ids = [2, 4, 5, 6, 12]
    prediction_length = 36

    sites_data_without_covariates = preprocessing_autogluon.get_autogluon_compatible_sites_independent_dfs_without_covariates()
    for site_id in sites_ids:
        model_training.train_model(
            sites_data_without_covariates.get(site_id), 
            prediction_length, 
            f'{common_path}/models/separate/{site_id}', 
            f'{common_path}/predictions/separate/{site_id}.csv', 
            metric
        )
    print('Best quality separate models trained and predictions made.')

    sites_data_with_covariates = preprocessing_autogluon.get_autogluon_compatible_sites_independent_dfs()
    for site_id in sites_ids:
        model_training.train_model(
            sites_data_with_covariates.get(site_id), 
            prediction_length, 
            f'{common_path}/models/separate_exog/{site_id}', 
            f'{common_path}/predictions/separate_exog/{site_id}.csv', 
            metric
        )
    print('Best quality separate models with exogenous features trained and predictions made.')

    unified_data_without_covariates = preprocessing_autogluon.get_autogluon_compatible_unified_df_without_covariates()
    model_training.train_model(
        unified_data_without_covariates, 
        prediction_length, 
        f'{common_path}/models/unified', 
        f'{common_path}/predictions/unified.csv', 
        metric
    )
    print('Best quality unified model trained and predictions made.')

    unified_data_with_covariates = preprocessing_autogluon.get_autogluon_compatible_unified_df()
    model_training.train_model(
        unified_data_with_covariates, 
        prediction_length, 
        f'{common_path}/models/unified_exog', 
        f'{common_path}/predictions/unified_exog.csv', 
        metric
    )
    print('Best quality unified model with exogenous features trained and predictions made.')
    print(f'All models trained and predictions made for metric {metric}.')

# Check and create directories if they do not exist
predictions_dir = '{common_path}/predictions'
separate_dir = os.path.join(predictions_dir, 'separate')
separate_exog_dir = os.path.join(predictions_dir, 'separate_exog')
os.makedirs(separate_dir, exist_ok=True)
os.makedirs(separate_exog_dir, exist_ok=True)

train_for_one_metric('WAPE')
#train_for_one_metric('MAE')
#train_for_one_metric('MSE')
#train_for_one_metric('RMSE')
