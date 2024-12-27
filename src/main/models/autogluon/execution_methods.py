import os
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
from datetime import datetime
import src.main.general.shared_variables as shared_variables
import src.main.general.data_importer as data_importer

hyperparameters = {
    'Theta':{'Theta': {}},
    'AutoARIMA': {'AutoARIMA': {}},
    'ChronosFineTunedWithRegressor[bolt_base]': {'Chronos': {
        'model_path': 'bolt_base',
        'covariate_regressor': 'CAT',
        'target_scaler': 'standard',
        'fine_tune': True,
        'ag_args': {'name_suffix': 'FineTunedWithRegressor'}
    }},
}

def _get_ag_main_dfs_with_covariates():
    sites_main_with_covariates = data_importer.get_imported_data()
    new_dictionary = {}
    for site_id, df in sites_main_with_covariates.items():
        new_df = df.rename(columns={'load_energy_sum': 'target', 'start_time': 'timestamp', 'site_id': 'item_id'})
        new_dictionary[site_id] = new_df
    return new_dictionary

def _get_ag_only_covariates_dfs():
    sites_main_with_covariates = data_importer.get_imported_data()
    new_dictionary = {}
    for site_id, df in sites_main_with_covariates.items():
        new_df = df.drop(columns=['target'])
        new_dictionary[site_id] = new_df
    return new_dictionary

def fit_predict_for_one(model_name, site_id, df, known_covariates):
    tsdf = TimeSeriesDataFrame.from_data_frame(df)
    train_data, test_data = tsdf.train_test_split(shared_variables.configuration['prediction_length'])
    predictor = TimeSeriesPredictor(
        prediction_length=shared_variables.configuration['prediction_length'],
        path=f'./autogluon_forecasts/{site_id}/{model_name}',
        target='target',
        eval_metric=shared_variables.configuration['eval_metric'],
        known_covariates_names=shared_variables.configuration['known_covariates_names'],
    )

    predictor.fit(
        train_data=train_data,
        time_limit=shared_variables.configuration['time_limit'],
        hyperparameters=hyperparameters[model_name],
        enable_ensemble=False,     
    )
    predictions = predictor.predict(data=train_data, known_covariates=known_covariates, model=f'{model_name}')
    predictions.to_csv(f'./autogluon_forecasts/{site_id}/{model_name}.csv')

def fit_predict():

    output_dir = f'{shared_variables.repo_path}autogluon_forecasts'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'autogluon_time_logs.txt')

    sites_main_with_covariates = _get_ag_main_dfs_with_covariates()
    sites_only_covariates = _get_ag_only_covariates_dfs()
    for site_id in shared_variables.sites_ids:
        for model_name in shared_variables.ag_model_names:
            with open(output_file, 'a') as f:
                f.write(f'{model_name} for site {site_id} started at {datetime.now()}\n')
            fit_predict_for_one(model_name, site_id, sites_main_with_covariates[site_id], sites_only_covariates[site_id])
            with open(output_file, 'a') as f:
                f.write(f'{model_name} for site {site_id} ended at {datetime.now()}\n')
