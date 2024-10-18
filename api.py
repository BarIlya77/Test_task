import openmeteo_requests
from sql import Weather, session


def add_weather_data(latitude, longitude):
    openmeteo = openmeteo_requests.Client()

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "precipitation", "pressure_msl", "wind_speed_10m", "wind_direction_10m"]
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()

    current_temperature_2m = round(current.Variables(0).Value(), 2)
    current_precipitation = round(current.Variables(1).Value(), 2)
    current_pressure_msl = round(current.Variables(2).Value(), 2)
    current_wind_speed_10m = round(current.Variables(3).Value(), 2)
    current_wind_direction_10m = round(current.Variables(4).Value(), 2)

    new_data = Weather(
        temperature=current_temperature_2m,
        precipitation=current_precipitation,
        pressure=current_pressure_msl,
        wind_speed=current_wind_speed_10m,
        wind_direction=wind_direction_convert(current_wind_direction_10m)
    )

    session.add(new_data)
    session.commit()


def wind_direction_convert(degrees):
    degrees = degrees % 360
    directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    index = round(degrees / 45) % 8

    return directions[index]