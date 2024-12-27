import src.main.general.data_importer as data_importer
import src.main.common_preprocessing.spikes_handler as spikes_handler
import src.main.common_preprocessing.exog_standardizer as exog_standardizer

def get_preprocessed_data():
    dfs = spikes_handler.get_sites_with_data_without_spikes(data_importer.get_imported_data())
    dfs = exog_standardizer.standardize_exog_data(dfs)    
    return dfs