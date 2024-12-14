import os
import pandas as pd
import matplotlib.pyplot as plt
import shared.shared_utility as shared_utility
import experiments.archive.sarimax.utility as sarimax_utility
import shared.preprocessing_general as preprocessing_general
import results.utility as results_utility

plots_dir = '/home/henri/Code/thesis-code/results/sarimax_plots'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

def load_data(file_path):
    return pd.read_csv(file_path, index_col=0, parse_dates=True)

def plot_data(actual, sarimax, site, variation):
    plt.figure(figsize=(12, 6))
    plt.plot(actual.index[-36:], actual['load_energy_sum'][-36:], label='Actual Consumption')
    plt.plot(actual.index[-36:], sarimax[variation]['mean'], label='SARIMAX Predictions')
    plt.title(f'SARIMAX - Site {site} variation: {variation}')
    plt.xlabel('Time')
    plt.ylabel('Electricity Consumption')
    plt.legend(loc='upper left')
    plot_filename = f'sarimax_site_{site}_{variation}.png'
    #plt.savefig(os.path.join(plots_dir, plot_filename))
    #plt.close()
    plt.show()

dfs = preprocessing_general.get_sites_with_data_wide()
dfs = preprocessing_general.convert_all_dfs_targets_to_megawatt_hours(dfs, 'load_energy_sum')

sarimax_predictions = results_utility.import_sarimax_predicitions()

for site in shared_utility.sites:
    actual = dfs[site]
    sarimax = sarimax_predictions[site]
    for variation in sarimax_utility.variations:
        plot_data(actual, sarimax, site, variation)