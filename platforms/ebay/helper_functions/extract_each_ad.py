from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import os
from googletrans import Translator
from openpyxl import Workbook
from PIL import Image
import requests
from io import BytesIO
from helper_functions_main import check_exists_by_xpath

def extract_each_ad(driver,new_urls,short_lead_name, real_name ,source_campaign,country,platform_name):

    ads = []
    i = 1

    screenshots_path = os.path.join('Output_data','Screenshoots',f'Proofs DB Preparator {short_lead_name}')
    os.mkdir(screenshots_path)

    workbook_name = f'ads_{real_name}.xlsx'
    wb = Workbook()
    page = wb.active
    page.title = 'ads'
    headers = ['Country','Seller name','Account name','Comments','Price','Title','Unit Sold','url','Products','Available unit','Offer Type','License Type','Lead_Source_Campaign','Platform','img_path']
    page.append(headers)

    p=1
    for url in new_urls:
        try:
            driver.get(url)
            
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='x-item-title__mainTitle']/span")))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@itemprop='price']/span")))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='vi-txt-underline']"))) 
            except Exception as e:
                print(url, "\n element not found \n",e)
                time.sleep(15)
            
            Country= country
            Seller_name= real_name
            Account_name= real_name
            url= url
            Products= np.nan

            try:
                Comments=driver.find_element_by_xpath("//h1[@class='x-item-title__mainTitle']/span").text
            except:
                Comments= np.nan
            try:
                Price= driver.find_element_by_xpath("//span[@itemprop='price']/span").text
            except: 
                Price= np.nan
            try:
                Title=driver.find_element_by_xpath("//h1[@class='x-item-title__mainTitle']/span").text
            except:
                Title= np.nan
             
            ############################# Unit Sold #############################
            Unit_Sold= np.nan
            if check_exists_by_xpath(driver, "//a[@class='vi-txt-underline']"):
                Unit_Sold= driver.find_element_by_xpath("//a[@class='vi-txt-underline']").text
                print('1 unit sold found')
            elif check_exists_by_xpath(driver, "//div[@class='d-quantity__availability']//a//font"):
                Unit_Sold= driver.find_element_by_xpath("//div[@class='d-quantity__availability']//a//font").text
                print('2 unit sold found')
            else:
                print('No unit sold found')
            
            ############################# Available unit #############################
            Available_unit= np.nan
            
            if check_exists_by_xpath(driver, "//span[@id='qtySubTxt']/span"):
                Available_unit= driver.find_element_by_xpath("//span[@id='qtySubTxt']/span").text
                print('1 Available unit found')
            elif check_exists_by_xpath(driver, "//span[@id='qtySubTxt']/span/font"):
                Available_unit= driver.find_element_by_xpath("//span[@id='qtySubTxt']/span/font").text
                print('2 Available unit found')
            elif check_exists_by_xpath(driver, "//div[@class='d-quantity__availability']//font"):
                Available_unit= driver.find_element_by_xpath("//div[@class='d-quantity__availability']//font").text
                print('3 Available unit found') 
            else:
                print('No Available unit found')
                
            ##########################################################################
            try:
                img_element = driver.find_element_by_xpath("//div[@class='ux-image-carousel-item active image']/img")
                img_url = img_element.get_attribute("src")
                i=1
                while True:
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))

                        img_path = os.path.join('Output_data','Imgs', f'{platform_name}_{short_lead_name}.jpg')
                        
                        if os.path.exists(img_path):
                            # Add a counter to the file name
                            file_name, file_ext = os.path.splitext(img_path)
                            counter = 1
                            new_img_path = file_name + str(counter) + file_ext
                            while os.path.exists(new_img_path):
                                counter += 1
                                new_img_path = file_name + str(counter) + file_ext
                            img_path = new_img_path
                        
                        try:
                            img.save(img_path, 'JPEG')
                            print(f'Image saved: {img_path}')
                            break
                        except:
                            print(f'Error saving image: {img_path}')
                            img_path = np.nan
                            break

                    elif i == 10:
                        print("Max attempt reached \n Error while fetching image, status code: ",response.status_code)
                        img_path = np.nan
                        break

            except Exception as e:
                print(e)
                img_path = np.nan

            Offer_Type=np.nan
            License_Type=np.nan
            Lead_Source_Campaign= source_campaign
            Platform= platform_name

            translator = Translator()
            Comments = translator.translate(Comments, dest='en').text
            Title = translator.translate(Title, dest='en').text
        except Exception as e:
            print(e)
            print(f'Error en esta parte de extrct each ad {url}')
            pass

        # escribir ad por ad en un excel
        row_values = []
        row_values.append(str(Country))
        row_values.append(str(Seller_name))
        row_values.append(str(Account_name))
        row_values.append(str(Comments))
        row_values.append(str(Price))
        row_values.append(str(Title))
        row_values.append(str(Unit_Sold))
        row_values.append(str(url))
        row_values.append(str(Products))
        row_values.append(str(Available_unit))
        row_values.append(str(Offer_Type))
        row_values.append(str(License_Type))
        row_values.append(str(Lead_Source_Campaign))
        row_values.append(str(Platform))
        
        # keep only the name of the image
        try:
            img_name = os.path.basename(img_path)
        except:
            img_name = np.nan

        row_values.append(str(img_name))
        
        page.append(row_values)

        ads_path = os.path.join('Output_data','Ads', workbook_name)
        wb.save(ads_path)

        #crear la carpeta de los snips y guardarlos
        title_folder = ''.join(c for c in url if c.isdigit())
        
        try:    
            single_screenshoot_path = os.path.join(screenshots_path, title_folder)
            os.mkdir(single_screenshoot_path)

            final_screenshoot_path = os.path.join(single_screenshoot_path, f'{platform_name}_{short_lead_name}_AllAds.png')
            driver.save_screenshot(final_screenshoot_path)
        except Exception as e:
            print(e)
            pass
        
        print(row_values)
        print('*'*50)
        print(f'Ad {p} extracted of {len(new_urls)}')
        print('*'*50)
        p += 1