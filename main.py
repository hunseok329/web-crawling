import requests
from bs4 import BeautifulSoup

URL = 'http://euler.synap.co.kr/prob_list.php'

def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class":"pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links:
        pages.append(link.string)
    return max(pages)
print(get_last_pages())