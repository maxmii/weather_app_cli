from wsgiref.simple_server import WSGIRequestHandler
from dotenv import load_dotenv
import os
import argparse
import sys
from urllib import parse
import requests
import simplejson as json

from style import Style

load_dotenv()


class WeatherConditions:

    def __init__(self):
        self.THUNDERSTORM = range(200, 300)
        self.DRIZZLE = range(300, 400)
        self.RAIN = range(500, 600)
        self.SNOW = range(600, 700)
        self.ATMOSPHERE = range(700, 800)
        self.CLEAR = range(800, 801)
        self.CLOUDY = range(801, 900)


class WeatherCLI:

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = os.getenv("WEATHER_URL")
        self.padding = 20

    def read_user_cli_args(self):
        """Handles the CLI user interactions.

        Returns:
            argparse.Namespace: Populated namespace object
        """
        parser = argparse.ArgumentParser(
            description="gets weather and temperature information for a city"
        )

        parser.add_argument(
            "city", nargs="+", type=str, help="enter a city name"
        )
        parser.add_argument(
            "-i",
            "--imperial",
            action="store_true",
            help="display the temperature in imperial units",
        )
        return parser.parse_args()

    def build_weather_query(self, city_input, imperial=False):
        """Builds the URL for an API request to OpenWeather's weather API.

        Args:
            city_input (List[str]): Name of a city as collected by argparse
            imperial (bool): Whether or not to use imperial units for temperature

        Returns:
            str: URL formatted for a call to OpenWeather's city name endpoint
        """

        api_key = self.api_key
        city_name = " ".join(city_input)
        url_encoded_city_name = parse.quote(city_name)
        units = "imperial" if imperial else "metric"
        url_request = f"{self.base_url}?q={url_encoded_city_name}&units={units}&appid={api_key}"
        return url_request

    def get_weather_data(self, query_url):
        """Makes an API request to a URL and returns the data as a Python object.

        Args:
            query_url (str): URL formatted for OpenWeather's city name endpoint

        Returns:
            dict: Weather information for a specific city
        """
        response = requests.get(query_url)
        if response.ok:
            pretty_json = json.loads(
                json.dumps(response.json(), indent=4, sort_keys=True)
            )
            return pretty_json
        else:
            match response.status_code:
                case 401:
                    sys.exit("Access denied. Check your API key.")
                case 404:
                    sys.exit("Can't find weather data for this city 😔")
                case _:
                    sys.exit(
                        f"Something went wrong... ({response.status_code})"
                    )

    def display_weather_info(self, weather_data, imperial=False):
        """Prints formatted weather information about a city.

        Args:
            weather_data (dict): API response from OpenWeather by city name
            imperial (bool): Whether or not to use imperial units for temperature

        More information at https://openweathermap.org/current#name
        """
        style = Style()
        city = weather_data["name"]
        weather_id = weather_data["weather"][0]["id"]
        weather_description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]

        style.change_colour(style.REVERSE)
        print(f"{city:^{style.PADDING}}", end="")
        style.change_colour(style.RESET)

        weather_symbol, colour = self._select_weather_display_params(
            weather_id
        )

        style.change_colour(colour)
        print(f"\t{weather_symbol}", end="")
        print(
            f"\t{weather_description.capitalize():^{style.PADDING}}",
            end=" ",
        )
        style.change_colour(style.RESET)

        style.change_colour(style.RESET)
        print(f"{temperature}°{'F' if imperial else 'C'}")

    def _select_weather_display_params(self, weather_id):
        """
        Selects the display parameters for a given weather condition.

        Args:
            weather_id (str): The weather condition identifier.

        Returns:
            tuple: A tuple containing the display symbol and the display style.

        """
        style = Style()
        weather_conditions = WeatherConditions()
        match weather_id:
            case weather if weather in weather_conditions.THUNDERSTORM:
                display_params = ("🌩", style.RED)
            case weather if weather in weather_conditions.DRIZZLE:
                display_params = ("💧", style.CYAN)
            case weather if weather in weather_conditions.RAIN:
                display_params = ("🌧️", style.BLUE)
            case weather if weather in weather_conditions.SNOW:
                display_params = ("⛄️", style.WHITE)
            case weather if weather in weather_conditions.ATMOSPHERE:
                display_params = ("🌀", style.BLUE)
            case weather if weather_id in weather_conditions.CLEAR:
                display_params = ("🌞", style.YELLOW)
            case weather if weather in weather_conditions.CLOUDY:
                display_params = ("💨", style.WHITE)
            case _:
                display_params = ("🌈", style.RESET)
        return display_params

    def check_temperature(self, temp, units="imperial"):
        # if units == "imperial":
        #     match temp:
        #         case
        # else:
        #     match temp:


if __name__ == "__main__":
    weather_cli = WeatherCLI()
    user_args = weather_cli.read_user_cli_args()
    user_url = weather_cli.build_weather_query(
        city_input=user_args.city,
        imperial=user_args.imperial,
    )
    weather_data = weather_cli.get_weather_data(user_url)
    weather_cli.display_weather_info(weather_data, user_args.imperial)
