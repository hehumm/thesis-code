import os
import pandas as pd
import shared.preprocessing_general as preprocessing_general
import experiments.final.final_shared as final_shared
import experiments.final.ag_predictions_importer as ag_predictions_importer
import shared.shared_utility as shared_utility

tables_dir = '/home/henri/Code/thesis-code/autogluon_tables'
if not os.path.exists(tables_dir):
    os.makedirs(tables_dir)

def generate_table(site, actual_consumption, theta_pred, ets_pred, autoarima_pred, chronos_zs_pred, chronos_ft_pred, chronos_wr_pred, chronos_ftwr_pred):
    table_data = {
        "Time": actual_consumption.index,
        "Actual Consumption": actual_consumption['load_energy_sum'].values,
        "Theta Predictions": theta_pred['mean'].values,
        "ETS Predictions": ets_pred['mean'].values,
        "AutoARIMA Predictions": autoarima_pred['mean'].values,
        "Chronos Zerp Shot Predictions": chronos_zs_pred['mean'].values,
        "Chronos Fine-Tuned Predictions": chronos_ft_pred['mean'].values,
        "Chronos With Regressor Predictions": chronos_wr_pred['mean'].values,
        "Chronos Fine-Tuned With Regressor Predictions": chronos_ftwr_pred['mean'].values,
    }
    table_data["Time"] = table_data["Time"].tz_localize(None)
    pd.DataFrame(table_data).to_excel(f'{tables_dir}/table_site_{site}.xlsx')

actual_dfs = preprocessing_general.get_sites_with_data_wide()
ag_predictions = ag_predictions_importer.import_ag_predictions()

for site in shared_utility.sites:
    actual_consumption = actual_dfs[site]
    generate_table(
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