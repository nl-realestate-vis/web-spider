import scrapy

class FundaSpider(scrapy.Spider):
    name = "immigrant"

    start_urls = [
        'http://www.allochtonenmeter.nl/?postcode=1315'
    ]

    def parse(self, response):

