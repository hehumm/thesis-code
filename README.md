# About

This is the repository containing my thesis' code

# Requirements for running the code

Create a `.env` file and add the location of the folder containing the testing data as `ROOT_DATA_FOLDER_PATH`.
The project expects the root folder to contain the folders `load_energy_sum`, `prices` and `weather`.
The files inside the folders should be named `{site_id}.json`. Provide a separate file for every site you want to use.

## Sample file structures:

### for `load_energy_sum`

```
[
  {
    "time_bucket": "2024-06-20 00:00:00+00",
    "load_energy_sum": "1417177218"
  },
  {
    "time_bucket": "2024-06-20 01:00:00+00",
    "load_energy_sum": "1341781923"
  },
]
```

### for `prices`

```
[
  {
    "start_time": "2024-06-20 00:00:00+00",
    "zoned_start_time": "2024-06-20 03:00:00",
    "buy_price_kwh": 15640,
    "sell_price_kwh": 7227
  },
  {
    "start_time": "2024-06-20 01:00:00+00",
    "zoned_start_time": "2024-06-20 04:00:00",
    "buy_price_kwh": 15517,
    "sell_price_kwh": 7126
  },
]
```

### for `weather`

```
[
  {
    "router_id": 2,
    "start_time": "2024-06-20 00:00:00+00",
    "end_time": "2024-06-20 01:00:00+00",
    "temp": "14.2",
    "feels_like": "13.32",
    "pop": 49,
    "clouds": 40,
    "sun_percentage": 0,
    "created_at": "2024-06-18 04:00:03.558618+00",
    "created_by": "system",
    "updated_at": null,
    "updated_by": null
  },
  {
    "router_id": 2,
    "start_time": "2024-06-20 01:00:00+00",
    "end_time": "2024-06-20 02:00:00+00",
    "temp": "13.89",
    "feels_like": "13.11",
    "pop": 0,
    "clouds": 38,
    "sun_percentage": 0,
    "created_at": "2024-06-18 04:00:03.558618+00",
    "created_by": "system",
    "updated_at": null,
    "updated_by": null
  },
]
```