import scrapy

class FundaSpider(scrapy.Spider):
    name = "funda"

    start_urls = [
        'https://www.funda.nl/en/koop/gouda/'
    ]

    def parse(self, response):
        # construct json from html source response
        for item in response.css('div.search-result-content'):
            yield {
                'address': item.css('h2.search-result__header-title::text').get(),
                'price': item.css('span.search-result-price::text').get(),
            }

        # scrape recursively until next page not available
        next_page = response.css('[rel=next]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

