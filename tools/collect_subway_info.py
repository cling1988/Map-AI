import os.path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless=new")  # for Chrome >= 109

html_file = "data/subway_page.html"
shop_info_file = "data/all_shop_info.csv"


def get_html():
    if not os.path.isfile(html_file):
        url = "https://subway.com.my/find-a-subway"
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url)
        html = browser.page_source
        with open(html_file, "w", encoding='utf-8') as file:
            file.write(html)
    else:
        with open(html_file, "r", encoding='utf-8') as file:
            html = file.read()
    return html


def read_html(html: str):
    soup = BeautifulSoup(html, 'lxml')
    shop_elements = soup.find_all("div", class_="fp_listitem")
    data_list = []
    print(len(shop_elements))
    for s in shop_elements:
        data = []
        # print(s)
        dla = s["data-latitude"]
        dlo = s["data-longitude"]
        name = s.find("h4")
        info = s.find("div", class_="infoboxcontent")
        all_info = info.find_all("p", class_=False)
        operation = []
        for index in range(1, len(all_info)):
            val = all_info[index].get_text(strip=True)
            if val:
                operation.append(val)
        data.append(name.get_text(strip=True))
        data.append(all_info[0].get_text(strip=True))
        data.append(",".join(operation))
        data.append(dla)
        data.append(dlo)
        data_list.append(data)
    return data_list


def write_file(data_list):
    df = pd.DataFrame(data_list, columns=['Name', 'Address', "Operation Hour", 'Latitude', 'Longitude'])
    df.to_csv(shop_info_file, index=False)
