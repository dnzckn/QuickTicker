import rumps
import threading
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

def get_temperature(driver):
    url = 'https://weather.com/weather/tenday/l/San+Diego+CA?canonicalCityId=cb5c473781cc06501376639dce8f0823a99187dcb42c79471a4303c076d66452'
    driver.get(url)
    temperature_element = driver.find_element(By.CSS_SELECTOR, 'span.DailyContent--temp--1s3a7')
    return temperature_element.text

def get_stock_price(driver):
    url = 'https://finance.yahoo.com/quote/AAPL/'
    driver.get(url)
    stock_price_element = driver.find_element(By.CSS_SELECTOR, 'fin-streamer[data-symbol="AAPL"]')
    return stock_price_element.get_attribute('value')

def get_relative_humidity(driver):
    url = 'https://www.timeanddate.com/weather/usa/san-diego'
    driver.get(url)
    humidity_element = driver.find_element(By.XPATH, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[6]/td')
    return humidity_element.text

def update_values(driver):
    temperature = get_temperature(driver)
    # stock_price = get_stock_price(driver)
    humidity = get_relative_humidity(driver)
    text = f"{round(float(temperature.split('°')[0]),2)}°F | RH: {humidity}"
    app.title = text

class WeatherStockApp(rumps.App):
    def __init__(self):
        super(WeatherStockApp, self).__init__("Loading...")
        self.driver = webdriver.Chrome(options=get_chrome_options())
        self.timer = rumps.Timer(self.threaded_update, 60*5)  # Update every 5 minutes
        self.timer.start()

    def threaded_update(self, _):
        thread = threading.Thread(target=update_values, args=(self.driver,))
        thread.start()

    def run(self):
        super().run()
        self.driver.quit()  # Close the driver when the app exits

if __name__ == "__main__":
    app = WeatherStockApp()
    app.run()
