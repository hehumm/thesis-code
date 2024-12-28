import src.main.general.data_importer as data_importer
import src.main.common_preprocessing.spikes_handler as spikes_handler
import src.main.common_preprocessing.exog_standardizer as exog_standardizer

def get_preprocessed_data():
    dfs = spikes_handler.get_sites_with_data_without_spikes(data_importer.get_imported_data())
    dfs = exog_standardizer.standardize_exog_data(dfs)    
    return dfs

# only used for ACF and PACF plots; not for actually fitting a model
def get_stationary_preprocessed_data():
    preprocessed_data = get_preprocessed_data()
    for key in preprocessed_data:
        if key == 5:
            preprocessed_data[key] = preprocessed_data[key].diff().dropna()
    return preprocessed_data