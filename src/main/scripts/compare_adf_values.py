import experiments.final.general.data_importer as data_importer
import experiments.final.common_preprocessing.spikes_handler as spikes_handler
import experiments.final.models.skforecast.execution_methods as skf

vanilla_dfs = data_importer.get_imported_data()
skf.test_sites_for_stationarity(vanilla_dfs)

print()

dfs_without_spikes = spikes_handler.get_sites_with_data_without_spikes(vanilla_dfs)
skf.test_sites_for_stationarity(dfs_without_spikes)
