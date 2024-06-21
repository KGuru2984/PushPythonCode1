import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

service = Service(executable_path='./Browser/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.delete_all_cookies()
driver.get("https://accounts.google.com/InteractiveLogin/signinchooser?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&osid=1&passive=1209600&service=mail&ifkv=ARZ0qKJeIqB-Qz9QdK5wd2wln7tafp56lSmnDyfD7eQ3IpSwqkM-3z5APTUbbJscvuZm3SAo_dNQog&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
driver.find_element("id", "identifierId").send_keys("express2gk@gmail.com")
time.sleep(2)
driver.find_element("css selector", "button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.BqKGqe.Jskylb.TrZEUc.lw1w4b").click()
time.sleep(3)
# # driver.find_element("name", "Passwd").send_keys("rakesh#2911")
# driver.find_element("name", "Passwd").send_keys("rakesh#2911")
# time.sleep(3)
# driver.find_element("xpath", "//butto[text()='Next']").click()
# time.sleep(3)
driver.close()
print("Gmail login has been successfully completed")