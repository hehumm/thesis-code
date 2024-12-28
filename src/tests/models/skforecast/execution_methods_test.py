import unittest
import pandas as pd
import src.main.models.skforecast.execution_methods as execution_methods
import src.main.general.shared_variables as shared_variables

class ExecutionMethodsTest(unittest.TestCase):

    def setUp(self):
        self.load_energy_path = f'{shared_variables.repo_path}data/load_energy_sum/'
        self.prices_path = f'{shared_variables.repo_path}data/prices/'
        self.weather_path = f'{shared_variables.repo_path}data/weather/'

        self.energy_load_data = self._load_load_data(self.load_energy_path)
        self.prices_data = self._load_load_data(self.prices_path)
        self.weather_data = self._load_load_data(self.weather_path)

    def _load_load_data(self, file_dir):
        data = {}
        for site_id in shared_variables.sites_ids:
            with open(f'{file_dir}{site_id}.json', 'r') as file:
                data[site_id] = pd.read_json(file)
        return data

    def test_get_sk_formatted_data(self):
        # Given
        formatted_data = execution_methods._get_sk_formatted_data()

        # When
        for site_id, (y, exog) in formatted_data.items():
            energy_load_df = self.energy_load_data[site_id]
            original_y_head_in_megawatt_hours = [x / 1000000000 for x in energy_load_df['load_energy_sum'][0:9].to_numpy()]
            formatted_y_head = y.to_frame()['load_energy_sum'][0:9].to_numpy()

            prices_df = self.prices_data[site_id]

            weather_df = self.weather_data[site_id]

            # Then
            self.assertTrue((original_y_head_in_megawatt_hours == formatted_y_head).all())
            self.assertTrue(exog.reset_index()[['buy_price_kwh', 'sell_price_kwh']].equals(prices_df[['buy_price_kwh', 'sell_price_kwh']]))
            self.assertTrue(exog.reset_index()[['sun_percentage', 'feels_like', 'clouds', 'temp', 'pop']].equals(weather_df[['sun_percentage', 'feels_like', 'clouds', 'temp', 'pop']]))

if __name__ == '__main__':
    unittest.main()