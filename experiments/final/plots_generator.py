import os
import matplotlib.pyplot as plt
import shared.shared_utility as shared_utility
import experiments.final.results_dataset_generator as results_dataset_generator
import experiments.final.final_shared as final_shared

def plot_data():
    plots_dir = '/home/henri/Code/thesis-code/plots'
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    data = results_dataset_generator.get_summary()
    for site in shared_utility.sites:
        values = data[site]
        plt.figure(figsize=(24, 12))
        plt.plot(values['actual'].index[-(final_shared.configuration.get('prediction_length')*2):],
                 values['actual']['target'][-(final_shared.configuration.get('prediction_length')*2):], label='Mõõdetud tarbimine')
        plt.plot(values['Theta'].index, values['Theta']['mean'], label='Theta')
        plt.plot(values['ETS'].index, values['ETS']['mean'], label='ETS')
        plt.plot(values['AutoARIMA'].index, values['AutoARIMA']['mean'], label='AutoARIMA')
        plt.plot(values['Chronos'].index, values['Chronos']['mean'], label='Chronos')
        plt.plot(values['SARIMAX'].index, values['SARIMAX']['mean'], label='SARIMAX')
        plt.plot(values['LSTM'].index, values['LSTM']['mean'], label='LSTM')
        plt.title(f'Asukoht {site}')
        plt.xlabel('Aeg')
        plt.ylabel('Elektritarbimine (MWh)')
        plt.legend(loc='upper left')
        # plot_filename = f'plot_site_{site}.png'
        # plt.savefig(os.path.join(plots_dir, plot_filename))
        # plt.close()
        plt.show()
