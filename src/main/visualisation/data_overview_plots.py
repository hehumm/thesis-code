import os
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import src.main.general.data_importer as data_importer
import src.main.common_preprocessing.spikes_handler as spikes_handler
import src.main.common_preprocessing.preprocessed_data_provider as preprocessed_data_provider
import src.main.general.shared_variables as shared_variables

original_dfs = data_importer.get_imported_data()
all_sites_spikes = spikes_handler.find_spikes()

plots_dir = f'{shared_variables.repo_path}/plots'

def plot_vanilla_data():
    for site_id, df in original_dfs.items():
        plt.figure(figsize=(24, 12))
        plt.plot(df['load_energy_sum'])
        plt.title(f'Asukoha {site_id} elektritarbimine')
        plt.ylabel('Elektritarbimine (MWh)')
        plt.xlabel('Aeg')
        #plt.show()
        plot_filename = f'plot_site_{site_id}.png'
        plt.savefig(os.path.join(plots_dir, plot_filename), bbox_inches='tight')
        plt.close()

def plot_spikes():
    for site_id, spike in all_sites_spikes.items():
        plt.figure(figsize=(24, 12))
        plt.plot(original_dfs[site_id]['load_energy_sum'], label='Algandmed')
        plt.scatter(spike.index, spike['load_energy_sum'], c='tab:orange', label='Tuvastatud tipud')
        plt.title(f'Asukoha {site_id} elektritarbimine')
        plt.ylabel('Elektritarbimine (MWh)')
        plt.xlabel('Aeg')
        plt.legend(loc='upper left')
        # plt.show()
        plot_filename = f'plot_site_{site_id}_spikes.png'
        plt.savefig(os.path.join(plots_dir, plot_filename), bbox_inches='tight')
        plt.close()

def plot_preprocessed_data():
    interpolated_dfs = preprocessed_data_provider.get_preprocessed_data()
    for site_id, df in interpolated_dfs.items():
        plt.figure(figsize=(24, 12))
        plt.plot(df['load_energy_sum'])
        plt.title(f'Asukoha {site_id} elektritarbimine pärast tippude eemaldamist')
        plt.ylabel('Elektritarbimine (MWh)')
        plt.xlabel('Aeg')
        # plt.show()
        plot_filename = f'plot_site_{site_id}_preprocessed.png'
        plt.savefig(os.path.join(plots_dir, plot_filename), bbox_inches='tight')
        plt.close()

def plot_acf_pacf(dfs):
    for site_id, df in dfs.items():
        y = df['load_energy_sum']

        plt.figure(figsize=(12, 6))
        plt.subplot(121)
        plot_acf(y, lags=50, ax=plt.gca())
        plt.title(f'Site {site_id} ACF')

        plt.subplot(122)
        plot_pacf(y, lags=50, ax=plt.gca(), method='ywm')
        plt.title(f'Site {site_id} PACF')

        plt.tight_layout()
        plt.show()


# plot_vanilla_data()
# plot_spikes()
# plot_preprocessed_data()

#training_dfs, _ = preprocessing_sarimax.test_train_split(sites_wo_spikes)
#plot_acf_pacf(training_dfs)
