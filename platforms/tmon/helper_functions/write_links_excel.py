from openpyxl import Workbook
import os

def write_links_excel(elements,lead_name):
    workbook_name = f'links_{lead_name}.xlsx'
    wb = Workbook()
    page = wb.active
    page.title = 'links'

    urls = []

    for element in elements:
        try:
            url = element.get_attribute('href')
            urls.append(url)
            page.append([url])
            
            
        except:
            pass

    path = os.path.join('Output_data','Ads_links',workbook_name)
    wb.save(path) 

    all_urls = urls
    
    unique_urls = [*set(urls)]
    
    return unique_urls, all_urls