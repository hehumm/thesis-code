import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

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
    root_data_path = os.environ['ROOT_DATA_FOLDER_PATH']
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

def wide_to_long(sites_with_data_wide):
    sites_with_data_long = {}
    for site_id, df in sites_with_data_wide.items():
        df = df.reset_index()
        df = pd.melt(
            df, 
            id_vars=['start_time'], 
            value_vars=['load_energy_sum', 'buy_price_kwh', 'sell_price_kwh', 
                        'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage'])
        df = df.rename(columns={'start_time': 'timestamp', 'variable': 'item_id', 'value': 'target'})
        sites_with_data_long[site_id] = df
    return sites_with_data_long