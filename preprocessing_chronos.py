import preprocessing_general
import pandas as pd

def _set_chronos_compatible_column_names(sites_dictionary):
    new_dictionary = {}
    for site_id, df in sites_dictionary.items():
        new_df = df.rename(columns={'load_energy_sum': 'target', 'start_time': 'timestamp', 'site_id': 'item_id'})
        new_dictionary[site_id] = new_df
    return new_dictionary

def get_chronos_compatible_sites():
    sites_with_data_wide_general = preprocessing_general.get_sites_with_data_wide()
    sites_with_timestamp_not_as_index = {site_id: df.reset_index() for site_id, df in sites_with_data_wide_general.items()}
    sites_with_added_site_id_column = {site_id: df.assign(site_id=site_id) for site_id, df in sites_with_timestamp_not_as_index.items()}
    sites_with_chronos_compatible_column_names = _set_chronos_compatible_column_names(sites_with_added_site_id_column)
    sites_with_timezone_removed_from_timestamp = {site_id: df.assign(timestamp=df['timestamp'].dt.tz_localize(None)) for site_id, df in sites_with_chronos_compatible_column_names.items()}
    return sites_with_timezone_removed_from_timestamp

def get_chronos_compatible_unified_df():
    return pd.concat(get_chronos_compatible_sites().values(), ignore_index=True)
