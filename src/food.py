import bs4
import urllib3
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from settings import settings

url = "https://www.facebook.com/kubosvetaine"
delay = 5

def is_correct_img(img):
	return "p526x296" in img['src']

def get_higher_res_img(img):
    parent = img.parent
    while parent.name != 'a':
        parent = parent.parent

    link = parent['href']

    print(f"Querying {link}")

    options = webdriver.ChromeOptions()
    options.binary_location = settings['chrome_install_location']
    options.add_argument('--headless')
    # options.add_argument('--lang=lit')
    driver_location = settings['chrome_driver_location']
    driver = webdriver.Chrome(driver_location, chrome_options=options)
    driver.set_window_size(1920,1080)

    driver.get(link)

    time.sleep(delay)

    html = driver.page_source

    driver.close()

    soup = bs4.BeautifulSoup(html, 'html5lib')
    
    imgs = soup.find_all('img')

    return imgs[0]

def get_food():
	
    print(f"Querying {url}")
    options = webdriver.ChromeOptions()
    options.binary_location = settings['chrome_install_location']
    options.add_argument('--headless')
    # options.add_argument('--lang=lit')
    driver_location = settings['chrome_driver_location']
    driver = webdriver.Chrome(driver_location, chrome_options=options)
    driver.set_window_size(1920,1080)

    # driver = webdriver.Chrome(os.getcwd()+'/chromedriver')
    driver.get(url)

    time.sleep(delay)

    html = driver.page_source

    # resp = http.request('GET', '')
    # data = resp.data.decode('utf-8')
    # f = open('html.txt', 'w')
    # f.write(data)
    # f.close()
    # # print(data)
    soup = bs4.BeautifulSoup(html, 'html5lib')
    # print('test')
    imgs = soup.find_all('img')
    # print(imgs)

    driver.close()

    for img in imgs:
        if img['src'].startswith('https://z-p3-scontent.fkun2-1.fna.fbcdn.net/v/t39.30808-6/p') and 'height' in img.attrs and 'width' in img.attrs:
            return get_higher_res_img(img)['src']
     
    # for img in imgs:
    #     # print(img.string)
    #     # print(str(img.text))
    #     print(img['src'])

    return None    

    # for img in imgs:
    #     if is_correct_img(img):
    #         return img

