import pandas as pd
import experiments.final.general.shared_variables as shared_variables

def add_missing_index(df, start_time, end_time):
    all_time_buckets = pd.date_range(start_time, end_time, freq='h')
    missing_timestamps = all_time_buckets.difference(df.index)
    missing_df = pd.DataFrame(index=missing_timestamps, columns=df.columns)
    df = pd.concat([df, missing_df])
    return df.sort_index()

def drop_redundant_merged_df_columns(merged_df):
    merged_df = merged_df.drop(columns=['zoned_start_time', 'router_id', 'end_time', 'created_at', 'created_by', 'updated_at', 'updated_by'])
    return merged_df

def merge_one_sites_dataframes(load_df, price_df, weather_df):
    merged_df = pd.merge(load_df, price_df, left_index=True, right_on='start_time', how='inner')
    merged_df = pd.merge(merged_df, weather_df, left_on='start_time', right_on='start_time', how='inner')
    merged_df.set_index('start_time', inplace=True)
    return merged_df

def load_one_sites_dataframes(site):
    root_data_path = f'{shared_variables.repo_path}/data'
    load_energy_sum_folder_path = '/load_energy_sum'
    prices_path = '/prices'
    weather_path = '/weather'
    load_df = pd.read_json(f'{root_data_path}{load_energy_sum_folder_path}/{site}.json')
    price_df = pd.read_json(f'{root_data_path}{prices_path}/{site}.json')
    weather_df = pd.read_json(f'{root_data_path}{weather_path}/{site}.json')
    return load_df, price_df, weather_df

def add_missing_datetimes_to_load_df(load_df):
    load_df['time_bucket'] = pd.to_datetime(load_df['time_bucket'])
    load_df = load_df.set_index('time_bucket')
    load_df = add_missing_index(load_df, load_df.index.min(), load_df.index.max())
    return load_df

_sites_with_data = {}

def _import_data ():
    for site_id in shared_variables.sites_ids:
        load_df, price_df, weather_df = load_one_sites_dataframes(site_id)
        load_df = add_missing_datetimes_to_load_df(load_df)
        load_df['load_energy_sum'] = load_df['load_energy_sum'].apply(lambda x: int(x) if pd.notnull(x) else x)
        load_df = load_df.interpolate()
        merged_df = merge_one_sites_dataframes(load_df, price_df, weather_df)
        merged_df = drop_redundant_merged_df_columns(merged_df)
        _sites_with_data[site_id] = merged_df

def _get_data():
    if len(_sites_with_data) == 0:
        _import_data()
    return _sites_with_data

def get_imported_data():
    sites_with_data_wide_general = _get_data()
    sites_with_start_time_not_as_index = {site_id: df.reset_index() for site_id, df in sites_with_data_wide_general.items()}
    sites_with_added_site_id_column = {site_id: df.assign(site_id=site_id) for site_id, df in sites_with_start_time_not_as_index.items()}
    sites_with_timezone_removed_from_start_time = {site_id: df.assign(start_time=df['start_time'].dt.tz_localize(None)) for site_id, df in sites_with_added_site_id_column.items()}
    sites_with_load_energy_sum_in_mwh = {site_id: df.assign(load_energy_sum=df['load_energy_sum'] / 1000000000) for site_id, df in sites_with_timezone_removed_from_start_time.items()}
    return sites_with_load_energy_sum_in_mwh
