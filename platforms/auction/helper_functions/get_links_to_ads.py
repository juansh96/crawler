import time

def get_links_to_ads(driver):
    
    elements = []

    actual_page = 0

    pages = driver.find_elements_by_xpath("//div[@class='paging']//a")

    link_pages = [page.get_attribute('href') for page in pages]

    for link in link_pages[2:6]:

        driver.get(link)

        time.sleep(3)

        _elements = driver.find_elements_by_xpath("//ul[@class='type2']/li/p/a")

        for element in _elements:
            url = element.get_attribute('href')
            elements.append(url)

        actual_page = driver.find_element_by_xpath("//a[@class='current']").text

        print(f'la pagina actual es {actual_page}')

        time.sleep(3)

    return elements