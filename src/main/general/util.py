import src.main.general.shared_variables as shared_variables

def test_train_split(dfs):
    forecast_horizon = shared_variables.configuration.get('prediction_length')
    train_dfs = {}
    test_dfs = {}
    for site_id, df in dfs.items():
        train_dfs[site_id] = df[:-forecast_horizon]
        test_dfs[site_id] = df[-forecast_horizon:]
    return train_dfs, test_dfs