import sys
from PyQt5 import QtWidgets, QtCore  # Import QtCore here
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

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QtCore.QTimer()  # Use QtCore.QTimer here
        self.timer.timeout.connect(self.update_values)
        self.timer.start(60000)  # Update every 60 seconds
        self.update_values()  # Call once to initialize

    def initUI(self):
        self.label = QtWidgets.QLabel('Loading...', self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle('Weather and Stock Info')
        self.show()

    def update_values(self):
        temperature = get_temperature()
        stock_price = get_stock_price()
        current_time = get_current_time()
        text = f"Time: {current_time} | Temperature: {round(float(temperature.split('°')[0]),2)}°F | Apple Stock Price: {stock_price}"
        self.label.setText(text)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
