import rumps
import threading
import requests
from bs4 import BeautifulSoup

def get_temperature():
    url = 'https://weather.com/weather/tenday/l/San+Diego+CA?canonicalCityId=cb5c473781cc06501376639dce8f0823a99187dcb42c79471a4303c076d66452'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    temperature_element = soup.select_one('span.DailyContent--temp--1s3a7')
    return temperature_element.text

def get_stock_price():
    url = 'https://finance.yahoo.com/quote/AAPL/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    stock_price_element = soup.select_one('fin-streamer[data-symbol="AAPL"]')
    return stock_price_element['value']

def get_relative_humidity():
    url = 'https://www.timeanddate.com/weather/usa/san-diego'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    humidity_element = soup.select_one('table tbody tr:nth-child(6) td')
    return humidity_element.text

def update_values():
    temperature = get_temperature()
    # stock_price = get_stock_price()
    humidity = get_relative_humidity()
    text = f"{round(float(temperature.split('°')[0]),2)}°F | RH: {humidity}"
    app.title = text

class WeatherStockApp(rumps.App):
    def __init__(self):
        super(WeatherStockApp, self).__init__("Loading...")
        self.timer = rumps.Timer(self.threaded_update, 60*5)  # Update every 5 minutes
        self.timer.start()

    def threaded_update(self, _):
        thread = threading.Thread(target=update_values)
        thread.start()

if __name__ == "__main__":
    app = WeatherStockApp()
    app.run()
