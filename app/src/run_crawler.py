from tasks import fetch_news
from urls import news_urls
import time

def run_crawler():
    while True:
        for element in news_urls:
            url, site = element
            fetch_news.delay(url, site)
        time.sleep(10)

if __name__ == "__main__":
    run_crawler()
