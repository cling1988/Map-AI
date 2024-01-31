import os.path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

html_file = "data/postcode_page.html"
info_file = "data/kl_postcode.txt"


def get_html():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    if not os.path.isfile(html_file):
        url = "https://malaysiapostcode.com/states/Wilayah_Persekutuan_Kuala_Lumpur"
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
    elements = soup.select("div.item.col-md-2.mb-2")
    data_list = []
    print("total postcode :", len(elements))
    for item in elements:
        data_list.append(item.get_text(strip=True))
    return data_list


def write_file(postcode_list):
    with open(info_file, "w") as file:
        file.write(",".join(postcode_list))


if __name__ == "__main__":
    html = get_html()
    postcodes = read_html(html)
    write_file(postcodes)
