import scrapy
from scrapy.linkextractors import LinkExtractor 
 
class Item(scrapy.Item):
    product_name = scrapy.Field()
    screen = scrapy.Field()
 
class MacbookTgddSpider(scrapy.Spider):
    name = 'tgdd'
    allowed_domains = ['www.thegioididong.com']
    start_urls = ['https://www.thegioididong.com/dtdd/']

    all_url = []
 
    def parse(self, response):
        links = LinkExtractor().extract_links(response=response)
        for link in links:
            if 'dtdd' not in link.url:
                continue
            if link.url not in self.all_url:
                self.all_url.append(link.url)
                yield scrapy.Request(link.url, callback=self.parse_item)
            

    def parse_item(self, response):
        item = Item()
        item['product_name'] =  response.xpath('/html/body/section[1]/h1').extract()
        item['screen'] = response.xpath('/html/body/section[1]/div[3]/div[2]/div[5]/ul/li[1]/div/span[1]').extract()
        
        yield item
