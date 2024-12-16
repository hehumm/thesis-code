from skforecast.sarimax import Sarimax
from skforecast.recursive import ForecasterSarimax
from skforecast.model_selection import TimeSeriesFold
from skforecast.model_selection import grid_search_sarimax

def perform_grid_search(param_grid, y, exog):

    forecaster = ForecasterSarimax(
        regressor=Sarimax(order=(12, 1, 1), maxiter=200)
    )

    cv = TimeSeriesFold(
        steps = 24,
        initial_train_size = 24,
    )

    return grid_search_sarimax(
        forecaster = forecaster,
        y = y,
        exog = exog,
        param_grid = param_grid,
        cv = cv,
        metric = 'mean_absolute_percentage_error',
        return_best = True,
        n_jobs = 'auto',
        suppress_warnings_fit = True,
        verbose = False,
        show_progress = True
    )

