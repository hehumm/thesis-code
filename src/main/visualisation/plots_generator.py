import os
import matplotlib.pyplot as plt
import src.main.general.results_dataset_generator as results_dataset_generator
import src.main.general.shared_variables as shared_variables

def plot_results():
    plots_dir = f'{shared_variables.repo_path}/plots'
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    data = results_dataset_generator.get_summary()
    for site in shared_variables.sites_ids:
        values = data[site]
        plt.figure(figsize=(24, 12))
        plt.plot(values['actual'].index[-(shared_variables.configuration.get('prediction_length')*2):],
                 values['actual']['target'][-(shared_variables.configuration.get('prediction_length')*2):], label='Actual consumption')
        plt.plot(values['Theta'].index, values['Theta']['mean'], label='Theta')
        plt.plot(values['AutoARIMA'].index, values['AutoARIMA']['mean'], label='AutoARIMA')
        plt.plot(values['Chronos'].index, values['Chronos']['mean'], label='Chronos')
        plt.plot(values['SARIMAX'].index, values['SARIMAX']['mean'], label='SARIMAX')
        plt.plot(values['LSTM'].index, values['LSTM']['mean'], label='LSTM')
        plt.title(f'Site {site}')
        plt.xlabel('Time')
        plt.ylabel('Electricity consumption (MWh)')
        plt.legend(loc='upper left')
        plot_filename = f'plot_site_{site}.png'
        plt.savefig(os.path.join(plots_dir, plot_filename))
        plt.close()
        # plt.show()
