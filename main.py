import requests
from bs4 import BeautifulSoup
import csv

URL = 'http://euler.synap.co.kr/prob_list.php'

# pagination 부분에서 마지막 페이지로 가는 번호 추출


def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links:
        pages.append(link.string)
    return max(pages)


def get_problem_word(html):
    tda = html.find("td", {"style": "padding-left:5px;"})
    fir = html.find("div")
    try:
        anchor = tda.find("a").text
        number = fir.find("b").string
        parent = tda.next_sibling.next_sibling.find("div")
        human = parent.get_text(strip=True).strip("\t").strip("\n")
        return {"achor": anchor, "number": number, "human": human}
    except AttributeError:
        return None

# last_page 값을 받아서 모든 페이지로 이동하며 크롤링


def get_problems(last):
    problems = []
    for page in range(last):
        result = requests.get(f"{URL}?pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        table = soup.find("table", {"class": "grid"})
        tr = table.find_all('tr')

        for word in tr:
            problem = get_problem_word(word)
            if problem is not None:
                problems.append(problem)
    return problems


def get_jobs():
    last_page = get_last_pages()
    problems = get_problems(int(last_page))
    save_to_file(problems)

# get_problems에서 추출한 값을 csv형식으로 저장


def save_to_file(problem):
    file = open("project_Euler@kr.csv", encoding='UTF8', mode="w", newline='')
    writer = csv.writer(file)
    writer.writerow(["number", "problem", "human"])

    for word in problem:
        writer.writerow(list(word.values()))
    return


get_jobs()
