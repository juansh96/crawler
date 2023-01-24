from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import os
from googletrans import Translator
from openpyxl import Workbook

from helper_functions_main import check_exists_by_xpath
from helper_functions_main import save_img

def extract_each_ad(driver,urls,lead_name,source_campaign,country,platform_name):

    ads = []
    i = 1

    screenshots_path = os.path.join('Output_data','Screenshoots',f'Proofs DB Preparator {lead_name}')
    os.mkdir(screenshots_path)

    
    workbook_name = f'ads_{lead_name}.xlsx'
    wb = Workbook()
    page = wb.active
    page.title = 'ads'
    headers = ['Country','Seller name','Account name','Comments','Price','Title','Unit Sold','url','Products','Available unit','Offer Type','License Type','Lead_Source_Campaign','Platform','img_path']
    page.append(headers)

    
    for url in urls:
        try:
            driver.get(url)
            
            # Esta parte es porque nunca carga bien la primera pagina
            if i == 1:
                time.sleep(5)
                driver.get(url)
                time.sleep(5)
            
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='deal_tit']")))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//strong[@class='sale_price']")))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='total_purchase']")))
            except Exception as e:
                print(url,e)
                time.sleep(15)

            Country= country
            Seller_name= lead_name
            Account_name= lead_name
            url= url
            Products= np.nan
            Offer_Type=np.nan
            License_Type=np.nan
            Lead_Source_Campaign= source_campaign
            Platform= platform_name
            
            # Extracting the Title and Comments (are the same)
            try:
                Comments=driver.find_element_by_xpath("//h3[@class='deal_tit']/font/font").text
            except:
                Comments= np.nan
            
            Title= Comments
            
            # Extracting the Price
            if check_exists_by_xpath(driver,"//strong[@class='sale_price']/em/font/font"):
                try:
                    Price= driver.find_element_by_xpath("//strong[@class='sale_price']/em/font/font").text
                except: 
                    Price= np.nan
            else:
                try:
                    Price= driver.find_element_by_xpath("//strong[@class='sale_price']/em").text
                except: 
                    Price= np.nan

            # Extracting the Unit Sold
            if check_exists_by_xpath(driver,"//span[@class='total_purchase']/font/strong/font"):    
                try:
                    Unit_Sold= driver.find_element_by_xpath("//span[@class='total_purchase']/font/strong/font").text
                except:
                    Unit_Sold= np.nan
            else:
                try:    
                    Unit_Sold= driver.find_element_by_xpath("//span[@class='total_purchase']/strong").text
                except:
                    Unit_Sold= np.nan    
            
            # Extracting the Available unit
            try:
                Available_unit= driver.find_element_by_xpath("//span[@class='stock']/font/font").text # no tiene stock
            except:
                Available_unit= np.nan
            
            # Extracting the image
            img_xpath = "//picture[1]/img"
            
            img_path = save_img(driver, img_xpath, platform_name, url)

            # translate to english
            translator = Translator()
            Comments = translator.translate(Comments, dest='en').text
            Title = translator.translate(Title, dest='en').text
        except:
            continue

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
        if isinstance(img_path, (str, bytes, os.PathLike)):
            print(f'acà voy: {img_path}')
            img_name = os.path.basename(img_path)
        else:
            print(f'hubo error acá ******')
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

            final_screenshoot_path = os.path.join(single_screenshoot_path, f'{platform_name}_{lead_name}_AllAds.png')
            driver.save_screenshot(final_screenshoot_path)
        except Exception as e:
            print(e)
            continue
        
        print(row_values)
        print('*'*50)
        print(f'Ad {i} extracted of {len(urls)}')
        print('*'*50)
        i += 1