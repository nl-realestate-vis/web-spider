import scrapy

class FundaSpider(scrapy.Spider):
    name = "immigrant"

    # postal code range in the Netherlands is [1011, 9999]
    start_urls = ["http://www.allochtonenmeter.nl/?postcode=%s" % postcode for postcode in range(1011,10000)]

    def parse(self, response):
        inhabitants = int(response.css('div.calculation tr')[1].css('td::text')[1].get())
        immigrants = int(response.css('div.calculation tr')[2].css('td::text')[1].get())
        nonwestern_immigrants = int(response.css('div.calculation tr')[4].css('td::text')[1].get())

        if inhabitants is not None:
            yield {
                'postcode': response.url[-4:],
                'inhabitants': inhabitants,
                'immigrant_rate': round(immigrants/inhabitants, 3),
                'nonwestern_immigrant_rate': round(nonwestern_immigrants/inhabitants, 3),
            }
