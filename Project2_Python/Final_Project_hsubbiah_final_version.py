# DSC 510 Introduction to Programming
# Final Project
# Programming Assignment Final Project
# Author Hemalatha Subbiah
# 11/15/2022

import sys
import requests
from requests import HTTPError
import fontstyle


def main():
    choice = 'Want to check weather of your favorite city'
    print(fontstyle.apply(choice, 'bold/Italic/red/BLACK_BG'))
    zip_bool = input('Press 0 for zipcode or press any key to get by state : ')
    print(fontstyle.apply(zip_bool, 'bold/Italic/red/BLACK_BG'))
    org_unit = input('Press "C" Celsius or "F" or  Fahrenheit or enter for Kelvin : ')
    temp_unit = decide_unit(org_unit)
    print(temp_unit)
    if zip_bool == "0":
        get_weather_from_zip(temp_unit, org_unit)
    else:
        get_lonlat_from_country_and_city(temp_unit, org_unit)


def decide_unit(temp_unit):
    if temp_unit == "C":
        temp_unit = "metric"
    elif temp_unit == "F":
        temp_unit = "imperial"
    else:
        temp_unit = ""
    return temp_unit


def get_lonlat_from_country_and_city(temp_unit, org_unit):
    # API key here

    api_key = "6c1beee7d828f86b2f88f89e3d58bc10"
    lat = ""
    lon = ""

    # url variable to store url
    url = "https://api.openweathermap.org/geo/1.0/direct"

    # Give city name
    city_name = input("Enter city name : ")

    # Give State code
    state_code = input("Enter state code : ")

    # Give Country name
    country_code = "US"

    # complete url address
    complete_url = url + "?q=" + city_name + "," + state_code + "," + country_code + "&appid=" + api_key
    print(complete_url)
    try:
        response = requests.get(complete_url)
        jsonResponses = response.json()
        for jsonResponse in jsonResponses:
            lat = jsonResponse["lat"]
            lon = jsonResponse["lon"]
        if lat is None or lon is None:
            raise ValueError("Lon and Lat value not returned from API Call")
        get_weather_from_lon_lat(lat, lon, temp_unit, org_unit)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        main()
    except Exception as err:
        print(f'Other error occurred: {err}')
        main()
    finally:
        main()


def get_weather_from_lon_lat(lat, lon, temp_unit, org_unit):
    # API key here
    api_key = "6c1beee7d828f86b2f88f89e3d58bc10"
    jsonResponse = {}

    # url variable to store url
    url = "https://api.openweathermap.org/data/2.5/weather"

    # complete url address
    complete_url = url + "?lat=" + str(lat) + "&" + "lon=" + str(lon) + "&appid=" + api_key + "&units=" + temp_unit
    print(complete_url)
    try:
        response = requests.get(complete_url)
        jsonResponse = response.json()
        if response.status_code == 404:
            raise ValueError('Invalid CityName and State entered by User,try with zipcode')
        if response.status_code == 200 and sys.getsizeof(jsonResponse) == 0:
            raise ValueError('Invalid CityName and State entered by User,try with zipcode')
        build_output(jsonResponse, temp_unit, org_unit)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    finally:
        main()


def get_weather_from_zip(temp_unit, org_unit):
    # API key here
    api_key = "6c1beee7d828f86b2f88f89e3d58bc10"
    jsonResponse = {}
    # url variable to store url
    url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    zip_code = input("Enter  zipcode: ")

    # complete url address
    complete_url = url + "appid=" + api_key + "&q=" + zip_code + "&units=" + temp_unit
    #print(complete_url)
    try:
        response = requests.get(complete_url)
        jsonResponse = response.json()
        #print(jsonResponse)
        if response.status_code == 404:
            raise ValueError('Invalid ZipCode entered by User,try with city name')
        if response.status_code == 200 and sys.getsizeof(jsonResponse) == 0:
            raise ValueError('Invalid ZipCode entered by User,try with city name')
        build_output(jsonResponse, temp_unit, org_unit)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    except requests.HTTPError as errh:
        print("Http Error:", errh)
        print("size" + str(sys.getsizeof(jsonResponse)))
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    finally:
        main()


def build_output(jsonResponse, temp_unit, org_unit):
    try:
        mai = jsonResponse["main"]
        print("---------------------------------------------------")
        print("---- Weather for the City " + jsonResponse["name"] + " Today ----")
        print("---------------------------------------------------")
        print()
        print("Current Temperature (in " + org_unit + ") : " + str(round(mai["temp"], 2)))
        print("Feels like  (in " + org_unit + ") : " + str(round(mai["feels_like"], 2)))
        print("Current Humidity (in percentage) : " + str(mai["humidity"]))
        print("Current Pressure (in hPa unit)   : " + str(mai["pressure"]))
        print("Current Temp (in " + org_unit + ") : " + str(round(mai["temp"], 2)))
        print("Current Temp_max (in " + org_unit + ") : " + str(round(mai["temp_max"], 2)))
        print("Current Temp_min (in " + org_unit + ") : " + str(round(mai["temp_min"], 2)))
        print("Visibility : " + str(jsonResponse["visibility"] / 100) + "%")
        weather = jsonResponse["weather"]
        print("Weather_description : " + str(weather[0]["description"]))
        print("icon : " + str(weather[0]["icon"]))
        w = jsonResponse["wind"]
        print("Wind Degree : " + str(w["deg"]))
        print("Wind Gust (in meter/sec) : " + str(w["gust"]))
        print("Wind Speed (in meter/sec) : " + str(w["speed"]))
        print("Have a Nice Day:)")
        print("---------------------------------------------------")
    except KeyError as k:
        print(f'The value for field {k} is not known')
        print("The User entered invalid zipcode , city or State")
    except Exception as e:
        print("Exception thrown while formatting output")
        print(e)
    finally:
        main()


if __name__ == "__main__":
    msg = "*** Welcome to Weather World ***"
    print(fontstyle.apply(msg, 'bold/Italic/red/BLACK_BG'))
    main()
