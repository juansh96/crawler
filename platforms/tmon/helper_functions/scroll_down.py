import time

def scroll_down(driver):
    

    last_height = driver.execute_script("return document.body.scrollHeight")

    elements = []


    while True:
              
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            
            elements = driver.find_elements_by_xpath("//a[@class='anchor']")
            
            break

        last_height = new_height

    return elements