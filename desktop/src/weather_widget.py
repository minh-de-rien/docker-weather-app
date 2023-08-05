"""
TODO
"""
import requests
import pgi
pgi.require_version('Gtk', '3.0')
from pgi.repository import Gtk, GLib


API_KEY = '36b96764a95f3dd9318b355da07e1ae7'

class WeatherWidget(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Weather Widget')

        # Create a label to display the weather information
        self.label = Gtk.Label()
        self.label.set_name('weather-label')
        self.add(self.label)

        # Load and apply CSS styles
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('desktop/src/styles_desktop.css')

        context = self.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Update weather information every 10 seconds
        GLib.timeout_add_seconds(10, self.update_weather, 'Montreal')


    def update_weather(self, city_name):
        url = f'http://localhost:5000/weather?city={city_name}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()

            if 'error' in weather_data:
                self.label.set_text(f'Error: {weather_data["error"]}')
            else:
                print(weather_data)
                city_name = weather_data['city_name']
                temperature = weather_data['temperature']
                humidity = weather_data['humidity']
                wind_speed = weather_data['wind_speed']
                self.label.set_text(f'City: {city_name}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s')

        except requests.RequestException as e:
            self.label.set_text(f'Error fetching weather data: {str(e)}')


win = WeatherWidget()
win.connect('delete-event', Gtk.main_quit)
win.set_keep_above(True)  # Ensure the window stays on top
# win.set_decorated(False)  # Remove window decorations (optional)
win.set_default_size(200, 100)
win.show_all()

Gtk.main()