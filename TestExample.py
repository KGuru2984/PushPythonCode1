from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

APIEndpoint = 'https://jsonplaceholder.typicode.com/users'
service = Service(executable_path='./Browser/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# driver = webdriver.Chrome(r'C:\GK Data\pythonProject\PythonAPI\Browser\chromedriver.exe')
driver.get("https://www.google.com/")
print(driver.title)
search_bar = driver.find_element("name", "q")
search_bar.clear()
search_bar.send_keys("getting started with python")
# search_bar = driver.find_element("name", "btnK")
search_bar.send_keys(Keys.RETURN)
print(driver.current_url)
driver.get(APIEndpoint)
response = driver.page_source
print("API Response:", response)
driver.close()
