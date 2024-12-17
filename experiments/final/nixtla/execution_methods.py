import os
from datetime import datetime
import pandas as pd
from neuralforecast import NeuralForecast
from neuralforecast.models import LSTM
from neuralforecast.losses.pytorch import MAPE
import experiments.final.preprocessed_data as preprocessed_data
import experiments.final.final_shared as final_shared
import shared.shared_utility as shared_utility

def _get_nixtla_main_dfs_with_covariates():
    default_main_with_covariates = preprocessed_data.get_sites_independent_dfs_with_covariates()
    sites_main_with_covariates = {}
    for site, df in default_main_with_covariates.items():
        sites_main_with_covariates[site] = df.rename(columns={'timestamp': 'ds', 'target': 'y', 'item_id': 'unique_id'})
    return sites_main_with_covariates

def fit_predict():
    output_dir = final_shared.nixtla_forecasts_path
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'nixtla_time_logs.txt')

    sites_main_with_covariates = _get_nixtla_main_dfs_with_covariates()

    for site in shared_utility.sites:
        with open(output_file, 'a') as f:
            f.write(f'Fitting and predicting for site {site} started at {datetime.now()}\n')

        pred_len = final_shared.configuration.get('prediction_length')
        df = sites_main_with_covariates.get(site)
        df_train = df[:-pred_len]
        nf = NeuralForecast(
            models=[
                LSTM(
                    h=final_shared.configuration['prediction_length'],
                    loss=MAPE(),
                    futr_exog_list=final_shared.configuration['known_covariates_names'],
                    # encoder_dropout=0.2,
                    scaler_type='standard',
                )
            ],
            freq='h'
        )
        nf.fit(df_train)
        exog_test = df[-pred_len:].drop(columns=['y'])
        y_pred = nf.predict(futr_df=exog_test)

        y_pred.to_csv(f'{output_dir}/predictions_lstm_{site}.csv')

        with open(output_file, 'a') as f:
            f.write(f'Fitting and predicting for site {site} ended at {datetime.now()}\n')
            