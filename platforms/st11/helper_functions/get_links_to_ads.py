import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_links_to_ads(driver):

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@class='view_more_bar']")))
        driver.find_element_by_xpath("//a[@class='view_more_bar']").click()
        time.sleep(10)

    except:
        print('No "View all products" button found', driver.current_url)
        
    elements = []

    #while element present click on view more button selenium

    while True:

        if driver.find_elements_by_xpath("//a[@class='view_more_bar']"):

            try:

                driver.find_element_by_xpath("//a[@class='view_more_bar']").click()

                time.sleep(5)

            except:
                break
        
        else:
            break

    elements = driver.find_elements_by_xpath("//a[@class='store_product_link']")

    return elements


    
   
        