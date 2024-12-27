from sklearn.preprocessing import StandardScaler

def standardize_exog_data(dfs):
    for site_id, df in dfs.items():
        scaler = StandardScaler()
        df[['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']] = scaler.fit_transform(df[['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']])
    return dfs