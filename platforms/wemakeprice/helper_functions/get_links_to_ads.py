import time

def get_links_to_ads(driver):
    

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    elements = []


    while True:
            
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            
            elements = driver.find_elements_by_xpath("//div[@class='list_conts_wrap']/a")
            
            break

        last_height = new_height

    return elements