from scrapy import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
import datetime as dt
import locale
import json
from twisted.internet import reactor
import os


def today_date():
    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
    today_date = dt.date.today().strftime("%d_%B")
    today_date = today_date[1:] if today_date[0] == '0' else today_date
    return today_date


class TodaySpider(Spider):

    name = 'todayspider'
    # day_of_interest = input(
    #     'inserire il giorno per il quale si vogliono sapere i fatti principali\n' \
    #     'nella forma gg_mese (esempio: 28_febbraio, 1_aprile): ')
    start_urls = [f'https://it.wikipedia.org/wiki/{today_date()}']

    def parse(self, response):
        eventi_scraping = response.xpath('//*[@id="mw-content-text"]/div[1]/ul[1]').get()
        eventi = ''
        for i in eventi_scraping.split('<'): eventi += (i.split('>')[-1])
        item = dict()
        item["giorno"] = today_date()
        item["eventi"] = eventi
        
        filename = os.getcwd().replace("\\","/") + "/accade_oggi.txt"
        with open(filename, 'w') as f:
            f.write(item['eventi']) #json.dumps(item))

        return print("crawl terminato")


def crawler():
    runner = CrawlerRunner()
    d = runner.crawl(TodaySpider)
    d.addBoth(lambda _: reactor.stop())
    
    filename = os.getcwd().replace("\\","/") + "/accade_oggi.txt"
    with open(filename, 'r') as f:
        lines = f.readlines()
    crawler_response = ''
    for line in lines:
        crawler_response += line

    return crawler_response
