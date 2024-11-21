from sklearn.base import BaseEstimator, RegressorMixin
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX

class SARIMAXEstimator(BaseEstimator, RegressorMixin):
    def __init__(self, order=(1, 0, 0), seasonal_order=(1, 0, 0, 12), trend=None):
        self.order = order
        self.seasonal_order = seasonal_order
        self.trend = trend
        
    def fit(self, X, y):
        self.model = SARIMAX(y, order=self.order, seasonal_order=self.seasonal_order, trend=self.trend)
        self.results = self.model.fit(disp=False)
        return self

    def predict(self, X):
        return self.results.predict(start=X.index[0], end=X.index[-1])
