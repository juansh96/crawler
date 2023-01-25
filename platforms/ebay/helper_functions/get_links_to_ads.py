import time

def get_links_to_ads(driver):

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if driver.find_element_by_xpath("//a[contains(@class, 'str-marginals__footer')]"):
            driver.find_element_by_xpath("//a[contains(@class, 'str-marginals__footer')]").click()
      
    except:
        print('No "View all products" button found', driver.current_url)
             
    elements = []

    #while element present click on view more button selenium

    i=0

    while True:

        _elements = driver.find_elements_by_xpath("//div[@class='s-item__info clearfix']/a")

        for element in _elements[1:len(_elements)+1]: #the first element is empty
            url = element.get_attribute('href')
            elements.append(url)

        i += 1

        if i == 3:
            break
        
        elif driver.find_elements_by_xpath("//a[@type='next']"):

            try:

                driver.find_element_by_xpath("//a[@type='next']").click()
                
                time.sleep(5)

            except:
                break
        
        else:
            break

    return elements     