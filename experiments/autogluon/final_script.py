import os

import experiments.autogluon.one_site_training as one_site_training
import experiments.autogluon.preprocessing_autogluon as preprocessing_autogluon

common_path='/home/henri/Code/thesis-code/experiments/autogluon_presets'
#common_path='/root/code/thesis-code/experiments/autogluon_presets'

# possible metrics: 'MAE', 'WAPE', 'MSE', 'RMSE'
def train_for_one_metric(metric):
    sites_ids = [2, 4, 5, 6, 12]
    prediction_length = 24
    known_covariates_names = ['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']

    sites_main_with_covariates = preprocessing_autogluon.get_sites_independent_dfs_with_covariates()
    sites_only_covariates = preprocessing_autogluon.get_sites_independent_dfs_only_covariates()
    for site_id in sites_ids:
        one_site_training.train_and_predict_with_model(
            sites_main_with_covariates.get(site_id), 
            prediction_length, 
            f'{common_path}/models/separate_exog/{site_id}',
            f'{common_path}/models/separate_exog/{site_id}/predictions_1.csv',
            f'{common_path}/models/separate_exog/{site_id}/predictions_2.csv',
            f'{common_path}/models/separate_exog/{site_id}/predictions_3.csv',
            f'{common_path}/models/separate_exog/{site_id}/predictions_4.csv',
            known_covariates_names,
            sites_only_covariates.get(site_id),
            metric
        )
    print('\nSeparate models with exogenous features trained and predictions made.')

    print(f'All models trained and predictions made for metric {metric}.')

#train_for_one_metric('WAPE')
#train_for_one_metric('MAE')
#train_for_one_metric('MSE')
train_for_one_metric('RMSE')
