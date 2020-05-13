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

def get_problem_word(html):
    tda = html.find("td", {"style":"padding-left:5px;"})
    # number = html.find_all("div", {"style":"text-align:center;"})
    return tda

def get_problems(last):
    for page in range(last):
        result = requests.get(f"{URL}?pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        table = soup.find("table", {"class":"grid"})
        for word in table:
            problem = get_problem_word(word)
            print(problem)

def get_jobs():
    last_page = get_last_pages()
    get_problems(int(last_page))

get_jobs()