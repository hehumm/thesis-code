from sklearn.base import BaseEstimator, RegressorMixin
import numpy as np
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

class SARIMAXEstimator(BaseEstimator, RegressorMixin):
    def __init__(self, order=(1, 0, 0), seasonal_order=(1, 0, 0, 12), steps=24):
        self.order = order
        self.seasonal_order = seasonal_order
        self.steps = steps
        
    def fit(self, X, y):
        self.model = SARIMAX(y, order=self.order, seasonal_order=self.seasonal_order, exog=X)
        self.results = self.model.fit(maxiter=200, disp=False)
        return self

    def predict(self, X):
        return self.results.forecast(steps=self.steps, exog=X)
    
    def score(self, X, y):
        y_pred = self.predict(X)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        return -rmse  # We negate it since RandomizedSearchCV minimizes the score

