from selenium import webdriver
import os

def driver_setup():

    options = webdriver.ChromeOptions()
    prefs = {
    "translate_whitelists": {"ko":"en"},
    "translate":{"enabled":"true"}
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36")
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver_path = os.path.join("selenium_web_driver", "chromedriver.exe")
    driver = webdriver.Chrome(executable_path= driver_path, options=options)

    return driver