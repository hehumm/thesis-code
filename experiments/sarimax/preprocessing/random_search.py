from sklearn.model_selection import RandomizedSearchCV
from experiments.sarimax.sk_wrapper import SARIMAXEstimator

# Define parameter grid for the SARIMAX model
param_dist = {
    'order': [(p, d, q) for p in range(1, 3) for d in range(1, 2) for q in range(1, 3)],
    'seasonal_order': [(P, D, Q, s) for P in range(1, 2) for D in range(1, 2) for Q in range(1, 2) for s in [12, 24]],
    'trend': [None, 'c', 't']
}

# Create an instance of the custom SARIMAX model
sarimax = SARIMAXEstimator()

# Perform RandomizedSearchCV
random_search = RandomizedSearchCV(sarimax, param_distributions=param_dist, n_iter=50, cv=3, n_jobs=-1)
random_search.fit(X_train, y_train)
