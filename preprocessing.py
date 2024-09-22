import utility

sites_with_data_wide = {}

def _import_data ():
    sites_ids = [2, 4, 5, 6, 12]

    for site_id in sites_ids:
        load_df, price_df, weather_df = utility.load_one_sites_dataframes(site_id)
        load_df = utility.add_missing_datetimes_to_load_df(load_df)
        merged_df = utility.merge_one_sites_dataframes(load_df, price_df, weather_df)
        merged_df = utility.drop_redundant_merged_df_columns(merged_df)
        sites_with_data_wide[site_id] = merged_df

def get_sites_with_data_wide():
    if len(sites_with_data_wide) == 0:
        _import_data()
    return sites_with_data_wide

def get_sites_with_data_long():
    if len(sites_with_data_wide) == 0:
        _import_data()
    return utility.wide_to_long(sites_with_data_wide)
