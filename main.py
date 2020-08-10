import time
import webbrowser

import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier


def fetch_articles():
    url = 'https://gall.dcinside.com/board/lists?id=programming'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    gall_list_table = soup.find('table', class_='gall_list')
    gall_article_trs = gall_list_table.find_all('tr', class_='us-post')

    articles = []

    for gall_article_tr in gall_article_trs:
        article_id = gall_article_tr.find('td', class_='gall_num').string
        article_title = gall_article_tr.find('td', class_='gall_tit').find('a').contents[1]

        article_author = gall_article_tr.find('td', class_='gall_writer').find('em').string
        article_span_ip = gall_article_tr.find('td', class_='gall_writer').find('span', class_='ip')
        if article_span_ip is not None:
            article_author += ' ' + article_span_ip.string

        article_created_at = gall_article_tr.find('td', class_='gall_date')['title']
        article_num_viewed = gall_article_tr.find('td', class_='gall_count').string
        article_num_recommended = gall_article_tr.find('td', class_='gall_recommend').string

        article = {
            'id': int(article_id),
            'title': article_title,
            'author': article_author,
            'created_at': article_created_at,
            'num_viewed': article_num_viewed,
            'num_recommended': article_num_recommended,
            'url': 'https://gall.dcinside.com/board/view/?id=programming&no=' + article_id
        }

        articles.append(article)

    return articles


def main():
    toast_notifier = ToastNotifier()

    last_id = 0

    while True:
        print("Fetching...")

        articles = fetch_articles()
        articles.sort(key=lambda e: e['id'])

        for article in articles:
            if last_id >= article['id']:
                continue

            if '방송' in article['title'] or '뱅송' in article['title']:
                toast_notifier.show_toast("방송 글 알림 - " + article['author'], article['title'],
                                          callback_on_click=lambda: webbrowser.open(article['url']))

        last_id = articles[-1]['id']

        time.sleep(10)


if __name__ == '__main__':
    main()