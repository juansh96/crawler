import time
import os
import pandas as pd
#estas son las mias

from platforms.auction.helper_functions.scroll_down import scroll_down
from platforms.auction.helper_functions.write_links_excel import write_links_excel
from platforms.auction.helper_functions.extract_each_ad import extract_each_ad
from helper_functions_main import driver_setup, short_name, links_leads


existent_links_path = os.path.join("Input_data","existent_links.xlsx")
existent_links = pd.read_excel(existent_links_path, sheet_name='CAPOC Sheet Advanced Find View')
existent_links = existent_links['URL'].tolist()


###################### Change this info for each lead ######################

platform = 'Auction'

list_lead_short_name, list_lead_real_name, list_source_campaign, list_country, list_profile_url = links_leads(platform)

driver = driver_setup()

try:
    for short_name, real_name, source_campaign, country, profile_url in zip(list_lead_short_name, list_lead_real_name, list_source_campaign, list_country, list_profile_url):

        short_lead_name = short_name

        real_name = real_name

        country = country

        source_campaign = source_campaign

        platform_name = platform

        print(f'Extrayendo links de: {real_name} \n Nombre corto: {short_lead_name} \n País: {country} \n Source campaign: {source_campaign} \n Plataforma: {platform_name}')

        # Going to the profile page
        driver.get(profile_url)

        time.sleep(5)

        # Extract the links to the ads

        elements = scroll_down(driver)

        print(f'El lead tiene publicados {len(elements)} anuncios (Incluyendo ads no pertenecientes a la campaña))')

        # Write the links to the excel file and remove duplicates

        unique_urls, all_urls = write_links_excel(elements,lead_name)

        print(f' Actualmente hay: {len(all_urls)} ads. \n De los cuales {len(unique_urls)} son únicos. \n {"*"*50} \n')

        #keep only the ads that are not in CRM

        new_urls = [url for url in unique_urls if url not in existent_links]

        print(f' Ads que no habian sido extraidos antes (No estan en el CRM): {len(new_urls)} \n {"*"*50} \n')

        #Visit each ad and extract info

        extract_each_ad(driver,new_urls,short_lead_name, real_name ,source_campaign,country,platform_name)

    driver.quit()
    print('Done')
    
    
except Exception as e:
    print(e)
    print(f'Error en el proceso del crawler de {platform} \n')
    driver.quit()




