import rumps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'")
    return chrome_options

def get_temperature():
    with webdriver.Chrome(options=get_chrome_options()) as driver:
        url = 'https://weather.com/weather/tenday/l/San+Diego+CA?canonicalCityId=cb5c473781cc06501376639dce8f0823a99187dcb42c79471a4303c076d66452'
        driver.get(url)
        temperature_element = driver.find_element(By.CSS_SELECTOR, 'span.DailyContent--temp--1s3a7')
        temperature = temperature_element.text
    return temperature

def get_stock_price():
    with webdriver.Chrome(options=get_chrome_options()) as driver:
        url = 'https://finance.yahoo.com/quote/AAPL/'
        driver.get(url)
        stock_price_element = driver.find_element(By.CSS_SELECTOR, 'fin-streamer[data-symbol="AAPL"]')
        stock_price = stock_price_element.get_attribute('value')
    return stock_price

def get_current_time():
    with webdriver.Chrome(options=get_chrome_options()) as driver:
        url = 'https://www.timeanddate.com/worldclock/usa/los-angeles'
        driver.get(url)
        time_element = driver.find_element(By.ID, 'ct')
        current_time = time_element.text
    return current_time

class WeatherStockApp(rumps.App):
    def __init__(self):
        super(WeatherStockApp, self).__init__("Loading...")
        self.timer = rumps.Timer(self.update_values, 60*5)  # Update every 5 minutes
        self.timer.start()

    @rumps.timer(60)
    def update_values(self, _):
        temperature = get_temperature()
        # stock_price = get_stock_price()
        # current_time = get_current_time()
        # text = f"Time: {current_time} | Temp: {round(float(temperature.split('°')[0]),2)}°F | AAPL: {stock_price}"
        text = f"{round(float(temperature.split('°')[0]),2)}°F"

        self.title = text

if __name__ == "__main__":
    app = WeatherStockApp()
    app.run()
