import scrapy


class FundaSpider(scrapy.Spider):
    name = "funda"

    start_urls = [
        'https://www.funda.nl/en/koop/amsterdam/p1/',
        'https://www.funda.nl/en/koop/amsterdam/p2/',
    ]

    def parse(self, response):
        for item in response.css('div.search-result-content'):
            yield {
                'address': item.css('h2.search-result__header-title::text').get(),
                'price': item.css('span.search-result-price::text').get(),
            }

