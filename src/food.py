import bs4
import urllib3
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from settings import settings

url = "https://www.facebook.com/kubosvetaine"

def get_food():
    options = webdriver.ChromeOptions()
    options.binary_location = settings['chrome_install_location']
    options.add_argument('--headless')
    driver_location = settings['chrome_driver_location']
    driver = webdriver.Chrome(driver_location, chrome_options=options)
    driver.set_window_size(1920,1080)

    # driver = webdriver.Chrome(os.getcwd()+'/chromedriver')
    driver.get(url)

    time.sleep(5)

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
    # for img in soup.find_all('img', {'class': ['i09qtzwb', 'n7fi1qx3', 'datstx6m', 'pmk7jnqg', 'j9ispegn', 'kr520xx4', 'k4urcfbm', 'bixrwtb6']}):
    # print(imgs[-1]['src'])
    # for img in imgs:
    #     # print(img.string)
    #     # print(str(img.text))
    #     print(img['src'])

    driver.close()

    img = imgs[-1]['src']

    return img