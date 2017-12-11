from selenium import webdriver

driverLocation = ""
browser = webdriver.Firefox()
browser.get("http://www.baidu.com")

print(browser.page_source)
browser.close()
