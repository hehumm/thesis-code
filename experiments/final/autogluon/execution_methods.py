import os
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
from datetime import datetime
import experiments.final.preprocessed_data as preprocessed_data
import experiments.final.final_shared as final_shared

hyperparameters = {
    'Theta':{'Theta': {}},
    'ETS': {'ETS': {}},
    'AutoARIMA': {'AutoARIMA': {}},
    'ChronosFineTunedWithRegressor[bolt_base]': {'Chronos': {
        'model_path': 'bolt_base',
        'covariate_regressor': 'CAT',
        'target_scaler': 'standard',
        'fine_tune': True,
        'ag_args': {'name_suffix': 'FineTunedWithRegressor'}
    }},
}

def fit_predict_for_one(model_name, site_id, df, known_covariates):
    tsdf = TimeSeriesDataFrame.from_data_frame(df)
    train_data, test_data = tsdf.train_test_split(final_shared.configuration['prediction_length'])
    predictor = TimeSeriesPredictor(
        prediction_length=final_shared.configuration['prediction_length'],
        path=f'./autogluon_forecasts/{site_id}/{model_name}',
        target='target',
        eval_metric=final_shared.configuration['eval_metric'],
        known_covariates_names=final_shared.configuration['known_covariates_names'],
    )

    predictor.fit(
        train_data=train_data,
        time_limit=final_shared.configuration['time_limit'],
        hyperparameters=hyperparameters[model_name],
        enable_ensemble=False,     
    )
    predictions = predictor.predict(data=train_data, known_covariates=known_covariates, model=f'{model_name}')
    predictions.to_csv(f'./autogluon_forecasts/{site_id}/{model_name}.csv')

def fit_predict():

    output_dir = '/home/henri/Code/thesis-code/autogluon_forecasts'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'autogluon_time_logs.txt')

    sites_ids = [2, 4, 5, 6, 12]

    sites_main_with_covariates = preprocessed_data.get_sites_independent_dfs_with_covariates()
    sites_only_covariates = preprocessed_data.get_sites_independent_dfs_only_covariates()
    for site_id in sites_ids:
        for model_name in final_shared.ag_model_names:
            with open(output_file, 'a') as f:
                f.write(f'{model_name} for site {site_id} started at {datetime.now()}\n')
            fit_predict_for_one(model_name, site_id, sites_main_with_covariates[site_id], sites_only_covariates[site_id])
            with open(output_file, 'a') as f:
                f.write(f'{model_name} for site {site_id} ended at {datetime.now()}\n')


