import os
import pandas as pd
import matplotlib.pyplot as plt

current_path = os.getcwd()

# Define the metrics and data variations
metrics = ['mae', 'mse', 'rmse', 'wape']
data_variations = ['separate', 'separate_exog', 'unified', 'unified_exog']
sites = [2, 4, 5, 6, 12]
last_168_hours = 168
prediction_horizon = 36

# Create the plots directory if it doesn't exist
plots_dir = 'plots'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

# Function to load data

def load_data(file_path):
    return pd.read_csv(file_path, index_col=0, parse_dates=True)

# Function to plot data
def plot_data(actual, chronos, weighted_ensemble, autoarima, metric, data_variation, site):
    plt.figure(figsize=(12, 6))
    plt.plot(actual.index[-last_168_hours:], actual[-last_168_hours:]['target'], label='Actual Consumption')
    plt.plot(actual.index[-prediction_horizon:], chronos['mean'], label='Chronos Predictions')
    plt.plot(actual.index[-prediction_horizon:], weighted_ensemble['mean'], label='WeightedEnsemble Predictions')
    plt.plot(actual.index[-prediction_horizon:], autoarima['mean'], label='AutoARIMA Predictions')
    plt.title(f'{metric} - {data_variation}' + (f' - Site {site}' if site else ''))
    plt.xlabel('Time')
    plt.ylabel('Electricity Consumption')
    plt.legend(loc='upper left')
    plot_filename = f'{metric}_{data_variation}_site_{site}.png'
    plt.savefig(os.path.join(plots_dir, plot_filename))
    plt.close()


for metric in metrics:
    chronos_folder = 'models/chronos'
    others_folder = 'models/others'
    for variation in data_variations:
        if 'unified' not in variation:
            for site in sites:
                actual_file = f'{current_path}/{site}_actual_data.csv'
                chronos_file = f'{current_path}/{metric}/{chronos_folder}/{variation}/{site}/predictions_1.csv'
                weighted_ensemble_file = f'{current_path}/{metric}/{others_folder}/{variation}/{site}/predictions_1.csv'
                autoarima_file = f'{current_path}/{metric}/{others_folder}/{variation}/{site}/predictions_2.csv'
                actual = load_data(actual_file)
                chronos = load_data(chronos_file)
                weighted_ensemble = load_data(weighted_ensemble_file)
                autoarima = load_data(autoarima_file)
                plot_data(actual, chronos, weighted_ensemble, autoarima, metric, variation, site)
        else:
            actual_file = f'{current_path}/unified_actual_data.csv'
            chronos_file = f'{current_path}/{metric}/{chronos_folder}/{variation}/predictions_1.csv'
            weighted_ensemble_file = f'{current_path}/{metric}/{others_folder}/{variation}/predictions_1.csv'
            autoarima_file = f'{current_path}/{metric}/{others_folder}/{variation}/predictions_2.csv'
            actual = load_data(actual_file)
            chronos_unified = load_data(chronos_file)
            weighted_ensemble_unified = load_data(weighted_ensemble_file)
            autoarima_unified = load_data(autoarima_file)

            actual_list = [actual[actual['item_id'] == site] for site in sites]
            chronos_unified_list = [chronos_unified[chronos_unified.index == site] for site in sites]
            weighted_ensemble_unified_list = [weighted_ensemble_unified[weighted_ensemble_unified.index == site] for site in sites]
            autoarima_unified_list = [autoarima_unified[autoarima_unified.index == site] for site in sites]
            for i in range(len(sites)):
                plot_data(actual_list[i], chronos_unified_list[i], weighted_ensemble_unified_list[i], autoarima_unified_list[i], metric, variation, sites[i])
