# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# 指定一個已知可用的ChromeDriver版本，例如 95.0.4638.54
chrome_driver_version = "95.0.4638.54"

# 使用指定的ChromeDriver版本來初始化webdriver.Chrome()
chrome_driver_path = ChromeDriverManager(version=chrome_driver_version).install()
driver = webdriver.Chrome(service=ChromeService(chrome_driver_path))


driver.get("https://google.com")
driver.get_screenshot_as_file("1.png")
