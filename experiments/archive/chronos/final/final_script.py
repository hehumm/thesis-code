import os

import experiments.autogluon_presets.model_training as model_training
import experiments.autogluon.preprocessing_autogluon as preprocessing_autogluon

#common_path='/home/henri/Code/thesis-code/experiments/autogluon_presets'
common_path='/root/code/thesis-code/experiments/autogluon_presets'

# possible metrics: 'MAE', 'WAPE', 'MSE', 'RMSE'
def train_for_one_metric(metric):
    sites_ids = [2, 4, 5, 6, 12]
    prediction_length = 36
    known_covariates_names = ['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']

    sites_main_with_covariates = preprocessing_autogluon.get_sites_independent_dfs_with_covariates()
    sites_only_covariates = preprocessing_autogluon.get_sites_independent_dfs_only_covariates()
    for site_id in sites_ids:
        model_training.train_and_predict_with_model(
            sites_main_with_covariates.get(site_id), 
            prediction_length, 
            f'{common_path}/models/separate_exog/{site_id}',
            f'{common_path}/models/separate_exog/{site_id}/predictions_1.csv',
            f'{common_path}/models/separate_exog/{site_id}/predictions_2.csv',
            known_covariates_names,
            sites_only_covariates.get(site_id),
            metric
        )
    print('\nSeparate models with exogenous features trained and predictions made.')

    sites_only_main = preprocessing_autogluon.get_sites_independent_dfs_only_main()
    for site_id in sites_ids:
        model_training.train_and_predict_with_model(
            sites_only_main.get(site_id), 
            prediction_length, 
            f'{common_path}/models/separate/{site_id}', 
            f'{common_path}/models/separate/{site_id}/predictions_1.csv', 
            f'{common_path}/models/separate/{site_id}/predictions_2.csv', 
            [],
            None,
            metric
        )
    print('\nSeparate models trained and predictions made.')

    unified_main_with_covariates = preprocessing_autogluon.get_unified_df_with_covariates()
    unified_only_covariates = preprocessing_autogluon.get_unified_df_only_covariates()
    model_training.train_and_predict_with_model(
        unified_main_with_covariates, 
        prediction_length, 
        f'{common_path}/models/unified_exog', 
        f'{common_path}/models/unified_exog/predictions_1.csv', 
        f'{common_path}/models/unified_exog/predictions_2.csv', 
        known_covariates_names,
        unified_only_covariates,
        metric
    )
    print('\nUnified model with exogenous features trained and predictions made.')

    unified_only_main = preprocessing_autogluon.get_unified_df_only_main()
    model_training.train_and_predict_with_model(
        unified_only_main, 
        prediction_length, 
        f'{common_path}/models/unified',
        f'{common_path}/models/unified/predictions_1.csv',
        f'{common_path}/models/unified/predictions_2.csv',
        [],
        None,
        metric
    )
    print('\nUnified model trained and predictions made.')

    print(f'All models trained and predictions made for metric {metric}.')

train_for_one_metric('WAPE')
#train_for_one_metric('MAE')
#train_for_one_metric('MSE')
#train_for_one_metric('RMSE')
