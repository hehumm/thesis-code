#from ...shared import preprocessing_general
import shared.preprocessing_general as preprocessing_general
import pandas as pd

def _set_autogluon_compatible_column_names(sites_dictionary):
    new_dictionary = {}
    for site_id, df in sites_dictionary.items():
        new_df = df.rename(columns={'load_energy_sum': 'target', 'start_time': 'timestamp', 'site_id': 'item_id'})
        new_dictionary[site_id] = new_df
    return new_dictionary



def get_sites_independent_dfs_with_covariates():
    sites_with_data_wide_general = preprocessing_general.get_sites_with_data_wide()
    sites_with_timestamp_not_as_index = {site_id: df.reset_index() for site_id, df in sites_with_data_wide_general.items()}
    sites_with_added_site_id_column = {site_id: df.assign(site_id=site_id) for site_id, df in sites_with_timestamp_not_as_index.items()}
    sites_with_chronos_compatible_column_names = _set_autogluon_compatible_column_names(sites_with_added_site_id_column)
    sites_with_timezone_removed_from_timestamp = {site_id: df.assign(timestamp=df['timestamp'].dt.tz_localize(None)) for site_id, df in sites_with_chronos_compatible_column_names.items()}
    return sites_with_timezone_removed_from_timestamp

def get_sites_independent_dfs_only_covariates():
    return {site_id: df[['timestamp', 'item_id', 'sun_percentage', 'buy_price_kwh', 'feels_like', 'sell_price_kwh', 'clouds', 'temp', 'pop']] for site_id, df in get_sites_independent_dfs_with_covariates().items()}

def get_sites_independent_dfs_only_main():
    return {site_id: df.drop(columns=['sun_percentage', 'buy_price_kwh', 'feels_like', 'sell_price_kwh', 'clouds', 'temp', 'pop']) for site_id, df in get_sites_independent_dfs_with_covariates().items()}



def get_unified_df_with_covariates():
    return pd.concat(get_sites_independent_dfs_with_covariates().values(), ignore_index=True)

def get_unified_df_only_covariates():
    return get_unified_df_with_covariates()[['timestamp', 'item_id', 'sun_percentage', 'buy_price_kwh', 'feels_like', 'sell_price_kwh', 'clouds', 'temp', 'pop']]

def get_unified_df_only_main():
    return get_unified_df_with_covariates().drop(columns=['sun_percentage', 'buy_price_kwh', 'feels_like', 'sell_price_kwh', 'clouds', 'temp', 'pop'])
