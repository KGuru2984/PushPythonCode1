from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (assuming you have Chrome WebDriver installed)
driver = webdriver.Chrome()

try:
    # Navigate to your Angular application
    driver.get("http://localhost:4200")  # Update the URL if needed

    # Wait for the product list to be rendered
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'app-product-list')))

    # Wait for 3 seconds to ensure all product names are loaded
    time.sleep(3)

    # Get the list of product names
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'app-product-list li')
    product_names = [element.text for element in product_elements]

    # Output the product names
    print("Product Names:")
    for name in product_names:
        print(name)

finally:
    # Close the browser window
    driver.quit()
