import scrapy

class FundaSpider(scrapy.Spider):
    name = "funda"

    start_urls = [
        'https://www.funda.nl/en/koop/gouda/',
        # 'https://www.funda.nl/en/koop/heel-nederland/',
        # 'https://www.funda.nl/en/koop/provincie-noord-holland/',
    ]

    def parse(self, response):
        # construct json from html source response
        for item in response.css('li.search-result'):
            yield {
                'address': item.css('h2.search-result__header-title::text').get().strip(),
                'postCode': item.css('h4.search-result__header-subtitle::text').get().strip(),
                'price': item.css('span.search-result-price::text').get().strip(),
                'url': response.urljoin(item.css('[data-object-url-tracking=resultlist]::attr(href)').get()),
                'thumbnail': item.css('div.search-result-image').css('img::attr(src)').get(),
                'livingArea': item.css('span[title="Living area"]::text').get(),
                'plotSize': item.css('span[title="Plot size"]::text').get(),
                'rooms': item.css('ul.search-result-kenmerken').css('li::text')[-1].get(),
            }

        # scrape recursively until next page not available
        next_page = response.css('[rel=next]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

