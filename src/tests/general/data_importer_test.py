import pandas as pd
import numpy as np
import unittest
import src.main.general.data_importer as data_importer

class DataImporterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dfs = {}
        cls.sites_ids = [2, 4, 5, 6, 12]
        for site_id in cls.sites_ids:
            load_df, price_df, weather_df = data_importer.load_one_sites_dataframes(site_id)
            load_df = data_importer.add_missing_datetimes_to_load_df(load_df)
            cls.dfs[site_id] = (load_df, price_df, weather_df)

    def test_that_merged_dataframes_data_is_consistent_with_original_load_dataframes(self):
        # Given
        load_dfs = [load_df for (load_df, _, _) in self.dfs.values()]
        merged_dfs = [data_importer.merge_one_sites_dataframes(load_df, price_df, weather_df) for (load_df, price_df, weather_df) in self.dfs.values()]
        
        # When
        for i in range(len(load_dfs)):
            load_df = load_dfs[i]
            merged_df = merged_dfs[i]

            for current_datetime in load_df.index:
                original_energy_sum = load_df.loc[current_datetime]['load_energy_sum']
                merged_energy_sum = merged_df.loc[current_datetime]['load_energy_sum']
                # Then
                if not pd.isnull(original_energy_sum):
                    self.assertEqual(original_energy_sum, merged_energy_sum)    

    def test_that_merged_dataframes_data_is_consistent_with_original_prices_dataframes(self):
        # Given
        prices_dfs = [price_df for (_, price_df, _) in self.dfs.values()]
        merged_dfs = [data_importer.merge_one_sites_dataframes(load_df, price_df, weather_df) for (load_df, price_df, weather_df) in self.dfs.values()]
        
        # When
        for i in range(len(prices_dfs)):
            price_df = prices_dfs[i]
            merged_df = merged_dfs[i]

            original_prices = price_df['buy_price_kwh'].to_numpy()
            merged_prices = merged_df['buy_price_kwh'].to_numpy()
            # Then
            self.assertTrue(np.array_equal(original_prices, merged_prices))

    def test_that_merged_dataframes_data_is_consistent_with_original_weather_dataframes(self):
        # Given
        weather_dfs = [weather_df for (_, _, weather_df) in self.dfs.values()]
        merged_dfs = [data_importer.merge_one_sites_dataframes(load_df, price_df, weather_df) for (load_df, price_df, weather_df) in self.dfs.values()]
        
        # When
        for i in range(len(weather_dfs)):
            weather_df = weather_dfs[i]
            merged_df = merged_dfs[i]

            original_temperature = weather_df['temp'].to_numpy()
            merged_temperature = merged_df['temp'].to_numpy()
            # Then
            self.assertTrue(np.array_equal(original_temperature, merged_temperature))

    def test_that_merged_dataframe_has_no_missing_datetimes(self):
        # Given
        merged_dfs = [data_importer.merge_one_sites_dataframes(load_df, price_df, weather_df) for (load_df, price_df, weather_df) in self.dfs.values()]

        # When
        for merged_df in merged_dfs:
            # Then
            self.assertEqual(len(merged_df), len(pd.date_range(merged_df.index.min(), merged_df.index.max(), freq='h')))

if __name__ == '__main__':
    unittest.main()