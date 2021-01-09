import scrapy

class FundaSpider(scrapy.Spider):
    name = "funda"

    start_urls = [
        'https://www.funda.nl/en/koop/gouda/',
        # 'https://www.funda.nl/en/koop/heel-nederland/',
        # 'https://www.funda.nl/en/koop/provincie-noord-holland/',
    ]

    def parse(self, response):
        # collect urls of all listing real state items
        # if need to filter out house/appartment, should base on url
        urls = []
        for item in response.css('li.search-result'):
            urls.append(response.urljoin(item.css('[data-object-url-tracking=resultlist]::attr(href)').get()))
        
        # scrape every item on current page
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)

        # scrape every page
        next_page = response.css('[rel=next]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        # html source code contains a json including some data
        source_json = eval(response.css('main#content').css('script::text').get().replace('\r\n','').strip())

        yield {
            'address': response.css('span.object-header__title::text').get(),
            'post_code': source_json['postcode'],
            'place': source_json['plaats'],
            'price': source_json['vraagprijs'],
            'photo': response.css('div.object-media-foto').css('img::attr(src)').get(),
            'living_area': source_json['woonoppervlakte'],
            'year': source_json['bouwjaar'],
            'url': response.url,

            # TODO: fix, cannot get value from second page on
            # 'plot_size': response.css('span[title~=plot]+span::text').get(),
            # 'bedrooms': response.css('span[title~=bedrooms]+span::text').get(),
        }

