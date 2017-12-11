from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"C:/Users/home/chromedriver.exe")#webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
