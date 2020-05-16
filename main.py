import requests
from bs4 import BeautifulSoup
# 프로젝트 오일러 사이트 한국사이터에서 원본 사이트로 변경 중

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
    for page in range(last):
        result = requests.get(f"{URL}?pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        table = soup.find("table", {"class": "grid"})
        tr = table.find_all('tr')
        # 문제 타이틀 부분이 같이 크롤링 되어 get_problem_word 부분에서 크롤링이 실패함 clear
        # a 태그를 가져오는 부분에서 None 타입이 있는 부분이 있는데 그부분에서 string 값으로 변환 실패 clear
        # a 태그 안에 다른 태그 들이 포함되어 있는 a 태그가 있어 string 변화에서 NoneTpye 값이 나오게 됨 clear
        # div 태드 안에 있는 푼 사람 숫자를 가져와야함
        for word in tr:
            problem = get_problem_word(word)
            if problem is not None:
                print(problem)


def get_jobs():
    last_page = get_last_pages()
    get_problems(int(last_page))


get_jobs()
