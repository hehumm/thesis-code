import os
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error
import shared.preprocessing_general as preprocessing_general
import experiments.final.ag_predictions_importer as ag_predictions_importer
import shared.shared_utility as shared_utility
import experiments.final.final_shared as final_shared

metrics_dir = '/home/henri/Code/thesis-code/autogluon_metrics'
if not os.path.exists(metrics_dir):
    os.makedirs(metrics_dir)

def generate_metrics(site, actual_consumption, theta_pred, ets_pred, autoarima_pred, chronos_zs_pred, chronos_ft_pred, chronos_wr_pred, chronos_ftwr_pred):
    metrics_data = {
        "Model": ["Theta", "ETS", "AutoARIMA", "Chronos Zero Shot", "Chronos Fine-Tuned", "Chronos With Regressor", "Chronos Fine-Tuned With Regressor"],
        "MAPE": [
            mean_absolute_percentage_error(actual_consumption['load_energy_sum'], theta_pred['mean']),
            mean_absolute_percentage_error(actual_consumption['load_energy_sum'], ets_pred['mean']),
            mean_absolute_percentage_error(actual_consumption['load_energy_sum'], autoarima_pred['mean']),
            mean_absolute_percentage_error(actual_consumption['load_energy_sum'], chronos_zs_pred['mean']),
            mean_absolute_percentage_error(actual_consumption['load_energy_sum'], chronos_ft_pred['mean']),
            mean_absolute_percentage_error(actual_consumption['load_energy_sum'], chronos_wr_pred['mean']),
            mean_absolute_percentage_error(actual_consumption['load_energy_sum'], chronos_ftwr_pred['mean']),
        ],
        "RMSE": [
            root_mean_squared_error(actual_consumption['load_energy_sum'], theta_pred['mean']),
            root_mean_squared_error(actual_consumption['load_energy_sum'], ets_pred['mean']),
            root_mean_squared_error(actual_consumption['load_energy_sum'], autoarima_pred['mean']),
            root_mean_squared_error(actual_consumption['load_energy_sum'], chronos_zs_pred['mean']),
            root_mean_squared_error(actual_consumption['load_energy_sum'], chronos_ft_pred['mean']),
            root_mean_squared_error(actual_consumption['load_energy_sum'], chronos_wr_pred['mean']),
            root_mean_squared_error(actual_consumption['load_energy_sum'], chronos_ftwr_pred['mean']),
        ],
    }
    pd.DataFrame(metrics_data).to_excel(f'{metrics_dir}/metrics_site_{site}.xlsx')

actual_dfs = preprocessing_general.get_sites_with_data_wide()
ag_predictions = ag_predictions_importer.import_ag_predictions()

for site in shared_utility.sites:
    actual_consumption = actual_dfs[site]
    generate_metrics(
        site,
        actual_consumption[-final_shared.configuration.get('prediction_length'):],
        ag_predictions[site]['Theta'],
        ag_predictions[site]['ETS'],
        ag_predictions[site]['AutoARIMA'],
        ag_predictions[site]['ChronosZeroShot[bolt_tiny]'],
        ag_predictions[site]['ChronosFineTuned[bolt_tiny]'],
        ag_predictions[site]['ChronosWithRegressor[bolt_tiny]'],
        ag_predictions[site]['ChronosFineTunedWithRegressor[bolt_tiny]'],
    )