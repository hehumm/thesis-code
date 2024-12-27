import src.main.general.data_importer as data_importer
import src.main.common_preprocessing.spikes_handler as spikes_handler
import src.main.models.skforecast.execution_methods as skf
import src.main.general.shared_variables as shared_variables

vanilla_dfs = data_importer.get_imported_data()
dfs_without_spikes = spikes_handler.get_sites_with_data_without_spikes(vanilla_dfs)
adf_values = skf.test_sites_for_stationarity(dfs_without_spikes)

with open(f'{shared_variables.repo_path}adf_values.txt', 'w') as file:
    for key, value in adf_values.items():
        file.write(f'{key} p-value: {value[1]}\n')
