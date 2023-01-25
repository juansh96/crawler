from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import time
from selenium import webdriver
import os

def rename_platforms(x):
    if re.search('ebay',x.lower()):
        return 'ebay'

    elif re.search('11st', x.lower()):
        return 'st11'
    
    else:
        return x


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def short_name(string):
        return "".join(c for c in string if c.isascii())

leads_path = os.path.join("Input_data","leads_links.xlsx")

def  links_leads(platform):

    df = pd.read_excel(leads_path)
    
    df = df[df['Platform'].str.lower().str.contains(platform.lower())]
            
    df['short_name'] = df['Account Name (Seller Name) (Account)'].apply(short_name)
    
    list_lead_short_name = df['short_name'].tolist()

    list_lead_real_name = df['Account Name (Seller Name) (Account)'].tolist()

    list_source_campaign = df['Source_campaign'].tolist()

    list_country = df['Country'].tolist()

    list_profile_url = df['Profile_link'].tolist()

    return list_lead_short_name, list_lead_real_name, list_source_campaign, list_country, list_profile_url



def save_img(driver, img_xpath, platform_name, url):
    
    try:
                    
        img_element = driver.find_element_by_xpath(img_xpath)
        img_url = img_element.get_attribute("src")
        e = 1
        while True:
            
            response = requests.get(img_url)
            if response.status_code == 200:

                try:
                    img = Image.open(requests.get(img_url, stream=True).raw)
                except:
                    img = Image.open(BytesIO(response.content))

                img = img.convert('RGB')
                
                img_path = os.path.join('Output_data','Imgs', f'{platform_name}.jpg')

                if os.path.exists(img_path):
                    # Add a counter to the file name
                    file_name, file_ext = os.path.splitext(img_path)
                    counter = 1
                    new_img_path = file_name + str(counter) + file_ext
                    while os.path.exists(new_img_path):
                        counter += 1
                        new_img_path = file_name + str(counter) + file_ext
                    img_path = new_img_path
            
                if isinstance(img_path, (str, bytes, os.PathLike)):
                        # Save the image
                        img.save(img_path, 'JPEG')
                        print(f'img saved in {img_path}')
                        break
                
                elif e == 10:
                    print("Max attempt reached \n Error while fetching image, status code: ",response.status_code)
                    img_path = np.nan
                    break
                    
                
                else:
                    print("Error while fetching image, status code: ",response.status_code)
                    time.sleep(5)
                    e += 1
        
        return img_path

    except Exception as e:
        print(e)
        print(f'no se pudo descargar la imagen del ad {url}')
        img_path = np.nan
        return img_path


def driver_setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
    prefs = {
    "translate_whitelists": {
                            "ko":"en",
                            "fr":"en",
                            "de":"en",
                            "es":"en",
                            "it":"en",
                            },
    "translate":{"enabled":"true"}
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36")
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1380")

    driver_path = os.path.join("selenium_web_driver", "chromedriver.exe")
    driver = webdriver.Chrome(executable_path= driver_path, options=options)

    return driver


