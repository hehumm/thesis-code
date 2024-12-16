import os
from datetime import datetime
import pandas as pd
import experiments.final.skforecast.hyperparams_tuner as tuner
import experiments.final.skforecast.sarimax_config as config
import experiments.final.autogluon.preprocessing_autogluon as preprocessing_autogluon
import experiments.final.final_shared as final_shared
import shared.shared_utility as shared_utility

def _get_params_file_path():
    output_dir = '/home/henri/Code/thesis-code/sk_forecast_forecasts'
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, 'sarimax_params_finding_time_logs.txt')

def _generate_sarimax_orders(site, site_main, site_covariates):
    output_file = _get_params_file_path()
    with open(output_file, 'a') as f:
        f.write(f'Best params search for site {site} started at {datetime.now()}\n')

    y = pd.Series(data=site_main.set_index('timestamp')['target']).asfreq('h')
    exog = site_covariates.set_index('timestamp').drop(columns=['item_id']).asfreq('h')
    best_params = tuner.perform_grid_search(config.param_grids.get(site), y, exog)
    best_params.to_excel(f'best_params_{site}.xlsx')

    with open(output_file, 'a') as f:
        f.write(f'Best params search for site {site} ended at {datetime.now()}\n')

def fit_predict():
    sites_main = preprocessing_autogluon.get_sites_independent_dfs_only_main()
    sites_only_covariates = preprocessing_autogluon.get_sites_independent_dfs_only_covariates()

    for site in shared_utility.sites:
        pred_len = final_shared.configuration.get('prediction_length')
        site_main_train = sites_main[site][:-pred_len]
        site_covariates_train = sites_only_covariates[site][:-pred_len]
        #_generate_sarimax_orders(site, site_main_train, site_covariates_train)
        
