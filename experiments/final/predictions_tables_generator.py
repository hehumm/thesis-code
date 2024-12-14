import os
import pandas as pd
import matplotlib.pyplot as plt
import shared.preprocessing_general as preprocessing_general
import experiments.final.final_shared as final_shared
import experiments.final.ag_predictions_importer as ag_predictions_importer
import shared.shared_utility as shared_utility

tables_dir = '/home/henri/Code/thesis-code/autogluon_tables'
if not os.path.exists(tables_dir):
    os.makedirs(tables_dir)

def generate_table(site, actual_consumption, theta_pred, ets_pred, autoarima_pred, chronos_pred):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axis("tight")
    ax.axis("off")
    table_data = {
        "Time": actual_consumption.index,
        "Actual Consumption": actual_consumption['load_energy_sum'].values,
        "Theta Predictions": theta_pred['mean'].values,
        "ETS Predictions": ets_pred['mean'].values,
        "AutoARIMA Predictions": autoarima_pred['mean'].values,
        "Chronos Predictions": chronos_pred['mean'].values,
    }
    table_data["Time"] = table_data["Time"].tz_localize(None)
    pd.DataFrame(table_data).to_excel(f'{tables_dir}/table_site_{site}.xlsx')

actual_dfs = preprocessing_general.get_sites_with_data_wide()
ag_predictions = ag_predictions_importer.import_ag_predictions()

for site in shared_utility.sites:
    actual_consumption = actual_dfs[site]
    generate_table(site, actual_consumption[-final_shared.configuration.get('prediction_length'):], ag_predictions[site]['Theta'], ag_predictions[site]['ETS'], ag_predictions[site]['AutoARIMA'], ag_predictions[site]['Chronos[bolt_tiny]'])