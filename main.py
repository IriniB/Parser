import requests
from bs4 import BeautifulSoup
import certifi
import pandas as pd


def get_content_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    new_links = []
    for link in soup.find_all("a"):
        if 'ПУНЦЭМ_до 670кВт' in str(link.get('href')):
            new_links.append(link.get('href'))
    return new_links


def get_all_links():
    url_start = 'https://bashesk.ru/corporate/tariffs/unregulated/?'
    url_end = 'filter_name=&filter_date_from=01.07.2019&filter_date_to=01.06.2020'
    links = []
    links.extend(get_content_from_page(url_start + url_end))
    page_number = 2
    while page_number < 4:
        links.extend(get_content_from_page(url_start + 'PAGEN_1=' + str(page_number) + '&' + url_end))
        page_number += 1
    return links


def download_file(file_link):
    link_start = 'https://bashesk.ru'
    response = requests.get(link_start + file_link)
    file_name = file_link[file_link.rfind("/") + 1:]
    open('files/' + file_name, "wb").write(response.content)
    return file_name


def print_result(files):
    for file in files:
        df = pd.read_excel(r'files/' + file, sheet_name='1 ц.к. ')
        print(file + ':\t\t' + str(df.values.tolist()[29][15]))


all_links = get_all_links()
file_names = []
for link in all_links:
    file_names.append(download_file(link))
print_result(file_names)
