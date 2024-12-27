
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import experiments.final.general.data_importer as data_importer
import experiments.final.common_preprocessing.spikes_handler as spikes_handler
import experiments.final.common_preprocessing.preprocessed_data_provider as preprocessed_data_provider

original_dfs = data_importer.get_imported_data()
all_sites_spikes = spikes_handler.find_spikes()

def plot_vanilla_data():
    for site_id, df in original_dfs.items():
        plt.figure(figsize=(24, 12))
        plt.plot(df['load_energy_sum'])
        plt.title(f'Asukoht {site_id}')
        plt.ylabel('Elektritarbimine (MWh)')
    plt.show()

def plot_spikes():
    for site_id, spike in all_sites_spikes.items():
        plt.figure(figsize=(24, 12))
        plt.plot(original_dfs[site_id]['load_energy_sum'], label='Algandmed')
        plt.scatter(spike.index, spike['load_energy_sum'], c='tab:orange', label='Tuvastatud jõnksud')
        plt.title(f'Asukoht {site_id}')
        plt.ylabel('Elektritarbimine (MWh)')
        plt.legend(loc='upper left')
        plt.show()

def plot_preprocessed_data():
    interpolated_dfs = preprocessed_data_provider.get_preprocessed_data()
    for site_id, df in interpolated_dfs.items():
        plt.figure(figsize=(24, 12))
        plt.plot(df['load_energy_sum'])
        plt.title(f'Asukoht {site_id} jõnksudeta')
        plt.ylabel('Elektritarbimine (MWh)')
    plt.show()

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
plot_spikes()
# plot_preprocessed_data()

#training_dfs, _ = preprocessing_sarimax.test_train_split(sites_wo_spikes)
#plot_acf_pacf(training_dfs)
