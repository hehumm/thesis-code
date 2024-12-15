import os
import matplotlib.pyplot as plt
import shared.shared_utility as shared_utility
import shared.preprocessing_general as preprocessing_general
import experiments.final.final_shared as final_shared
import experiments.final.ag_predictions_importer as ag_predictions_importer


plots_dir = '/home/henri/Code/thesis-code/autogluon_plots'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

def plot_data(site, actual_consumption, theta_pred, ets_pred, autoarima_pred, chronos_zs_pred, chronos_ft_pred, chronos_wr_pred, chronos_ftwr_pred):
    plt.figure(figsize=(12, 6))
    plt.plot(actual_consumption.index, actual_consumption['load_energy_sum'], label='Actual Consumption')
    plt.plot(theta_pred.index, theta_pred['mean'], label='Theta Predictions')
    plt.plot(ets_pred.index, ets_pred['mean'], label='ETS Predictions')
    plt.plot(autoarima_pred.index, autoarima_pred['mean'], label='AutoARIMA Predictions')
    plt.plot(chronos_zs_pred.index, chronos_zs_pred['mean'], label='Chronos Zero Shot Predictions')
    plt.plot(chronos_ft_pred.index, chronos_ft_pred['mean'], label='Chronos Fine-Tuned Predictions')
    plt.plot(chronos_wr_pred.index, chronos_wr_pred['mean'], label='Chronos With Regressor Predictions')
    plt.plot(chronos_ftwr_pred.index, chronos_ftwr_pred['mean'], label='Chronos Fine-Tuned With Regressor Predictions')
    plt.title(f'Site {site}')
    plt.xlabel('Time')
    plt.ylabel('Electricity Consumption')
    plt.legend(loc='upper left')
    # plot_filename = f'autogluon_site_{site}.png'
    # plt.savefig(os.path.join(plots_dir, plot_filename))
    # plt.close()
    plt.show()

actual_dfs = preprocessing_general.get_sites_with_data_wide()
ag_predictions = ag_predictions_importer.import_ag_predictions()

for site in shared_utility.sites:
    actual_consumption = actual_dfs[site]
    plot_data(
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