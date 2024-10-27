import unittest
import shared.preprocessing_general as preprocessing_general
import shared.rolling_cross_validation as rolling_cross_validation

class TestUtility(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.dfs = preprocessing_general.get_sites_with_data_wide()
        return

    def test_splitter_split_df_equally_and_added_remaining_elements_to_last_split(self):
        # Given
        n_splits = 5
        df_length = len(self.dfs.get(2))
        # When
        actual_lengths = [len(split_df) for split_df in rolling_cross_validation._split_into_time_windows(self.dfs.get(2), n_splits)]
        expected_lengths = [df_length // n_splits] * (n_splits - 1) + [df_length // n_splits + df_length % n_splits]
        # Then
        self.assertEqual(actual_lengths, expected_lengths)
        return

    

if __name__ == '__main__':
    unittest.main()