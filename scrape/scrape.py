import requests
from bs4 import BeautifulSoup
import urllib3
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def proxy_generator(start=0):
    header = {
        'authority': 'hidemy.name',
        'method': 'GET',
        'path': '/ru/proxy-list/',
        'scheme': 'https',
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'referer': 'https://hidemy.name/ru/proxy-list/?start=1856',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.93 Safari/537.36 '
    }
    while True:
        if start >= 1000:
            start = 0
        response = requests.get(f'https://hidemy.name/ru/proxy-list/?maxtime=2500&start={start}', headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')
        for item in soup.find('tbody').find_all('tr'):
            yield ':'.join(map(lambda x: x.text, item.find_all('td')[:2]))
        print(f'______________________{start}____________________________')
        start += 64


def scrape_word():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36",
    }
    response_base = requests.get('https://bararanonline.com/').content
    soup = BeautifulSoup(response_base, 'html.parser')
    flag_ = True
    with open('encyclopedia.text', 'a', encoding='utf8') as file:
        for item in soup.find('div', {'class': 'content-letters col-xl-5 col-lg-5 col-md-5 col-sm-12'}).find_all('a')[
                    30:]:
            print(item['href'])
            if flag_:
                i = 46
                flag_ = False
            else:
                i = 41
            proxy_ = proxy_generator()
            ip = next(proxy_)
            flag = True
            with requests.session() as session:
                session.headers = headers
                count = 0
                while True:
                    if flag:
                        flag = False
                        proxy = {
                            'http': f'http://{ip}',
                            'https': f'https://{ip}'
                        }
                        session.proxies = proxy
                        session.trust_env = False
                    print(proxy)
                    try:
                        print(f"{item['href']}?page={i}")
                        response = session.get(f"{item['href']}?page={i}", timeout=5)
                        print(response.status_code)
                        if response.status_code == 404:
                            break
                        count = 0
                    except Exception as e:
                        print(e)
                        if count >= 3:
                            count = 0
                            flag = True
                            ip = next(proxy_)
                        sleep(1)
                        count += 1
                        continue
                    soup = BeautifulSoup(response.content, 'html.parser')
                    print(f"{item['href']}?page={i}")
                    try:
                        for word_a in soup.find('div', {'class': 'content-letters p-1'}).find_all('a',
                                                                                                  {
                                                                                                      'class': 'word-href'}):
                            word = word_a.text.strip('\n')
                            file.write(f"{word}\n")
                        print(word)
                    except AttributeError:
                        print('no')
                        flag = True
                        ip = next(proxy_)
                        continue
                    i += 1


if __name__ == '__main__':
    scrape_word()
