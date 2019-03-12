# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class NupepaSpider(scrapy.Spider):
    name = 'nupepa'
    allowed_domains = ['papakilodatabase.com/pdnupepa']
    start_urls = ['http://papakilodatabase.com/pdnupepa/?a=cl&cl=CL2']

    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def parse(self, response):
        month_xpath = '//div[@id="datebrowserrichardtoplevelcalendar"]/div/span/ul/li/a/@href'
        month_urls = response.xpath(month_xpath).extract()
        for url in month_urls:
            # Send a request for a page
            next_page = response.urljoin(url)
            yield scrapy.Request(next_page, callback = self.parse_month)

    def parse_month(self, response):
        # Get the date (e.g. ['February 1834'])
        date_xpath = '//div[@id="datebrowserrichardmonthlevelcalendarheader"]/h2/text()'
        date = response.xpath(date_xpath).extract()

        card_xpath = '//div[@class="card"]/ul/li/a/@href'
        cards = response.xpath(card_xpath).extract()

        for card in cards:
            # Send a request for a page
            next_page = response.urljoin(url)
            yield scrapy.Request(next_page, callback = self.parse_card)

    def parse_card(self, response):
        pass

