from datetime import date, datetime, timedelta
from demo import config
import requests

def call_owm_forecast(lat=52.1051, lon=-3.668, exclude='current,minutely,daily,alerts'):
    """
    Call OpenWeather API to get hourly weather forecast for the next 2 days. The location
    has been set to (52.1051, -3.668) by default.

    Args:
        lat (`float`, optional): Geographical coordinates, latitude. Defaults to 52.1051
        lon (`float`, optional): Geographical coordinates, longitude. Defaults to -3.668
        exclude (`str`, optional): Exlude data from API response. The options are:
            - `current`
            - `minutely`
            - `hourly`
            - `daily`
            - `alerts`

            The default is to exclude everything except `hourly`
    
    Returns:
        dict: JSON response from API call
    
    Raises:
        RuntimeError: If OWM_API_KEY is not defined.
    """
    if not config.OWM_API_KEY:
        raise RuntimeError('OWM_API_KEY is not specify, use export OWM_API_KEY <api-key>')

    url = 'https://api.openweathermap.org/data/2.5/onecall'
    resp = requests.get(url, params=dict(lat=lat, lon=lon,
                                         exclude=exclude,
                                         appid=config.OWM_API_KEY,
                                         units='standard'))
    resp.raise_for_status() # raise any HTTP error
    print(resp.text)
    return resp.json()

def call_owm_history(dt, lat=52.1051, lon=-3.668):
    """
    Call OpenWeather API to get historical weather data. The location has been set to
    (52.1051, -3.668) by default.

    Args:
        dt (`datetime.date`): Date from the previous five days (Unix time, UTC time zone).
        lat (`float`, optional): Geographical coordinates, latitude. Defaults to 52.1051
        lon (`float`, optional): Geographical coordinates, longitude. Defaults to -3.668
    
    Returns:
        dict: JSON response from API call
    
    Raises:
        RuntimeError: If OWM_API_KEY is not defined.
        ValueError: If dt exceeds the time range of 5 days.
    """
    if not config.OWM_API_KEY:
        raise RuntimeError('OWM_API_KEY is not specify, use export OWM_API_KEY <api-key>')
    if datetime.now().date() - timedelta(days=5) > dt:
        raise ValueError('"dt" must be within 5 days from now')

    url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'
    resp = requests.get(url, params=dict(lat=lat, lon=lon,
                                         dt=dt.strftime('%s'),
                                         appid=config.OWM_API_KEY,
                                         units='standard'))
    resp.raise_for_status() # raise any HTTP error

    return resp.json()
