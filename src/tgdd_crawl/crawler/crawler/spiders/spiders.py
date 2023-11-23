import scrapy
from scrapy.linkextractors import LinkExtractor 
import re

pattern = re.compile('<.*?>')

def clean(str):
    return re.sub(pattern, '', str)

class Item(scrapy.Item):
    link = scrapy.Field()
    product_name = scrapy.Field()
    screen = scrapy.Field()
    os = scrapy.Field()
    front_camera = scrapy.Field()
    camera = scrapy.Field()
    chip = scrapy.Field()
    ram = scrapy.Field()
    storage = scrapy.Field()
    sim = scrapy.Field()
    battery = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
        

 
class MacbookTgddSpider(scrapy.Spider):
    name = 'tgdd'
    allowed_domains = ['www.thegioididong.com']
    start_urls = ['https://www.thegioididong.com/dtdd#c=42&o=17&pi=5',
                  'https://www.thegioididong.com/dtdd#c=42&o=17&pi=1',
                  'https://www.thegioididong.com/dtdd#c=42&o=17&pi=2',
                  'https://www.thegioididong.com/dtdd#c=42&o=17&pi=3',
                  'https://www.thegioididong.com/dtdd#c=42&o=17&pi=4',
                  'https://www.thegioididong.com/dtdd']

    all_url = []
    num_page = 0
 
    def parse(self, response):
        links = LinkExtractor().extract_links(response=response)

        for link in links:
            if 'dtdd' not in link.url:
                continue
            if link.url not in self.all_url:
                self.all_url.append(link.url)
                if '/dtdd/' in link.url:
                    yield scrapy.Request(link.url, callback=self.parse_item)
                elif '/dtdd' in link.url:
                    yield scrapy.Request(link.url, callback=self.parse)


    def parse_item(self, response):
        item = Item()
        item['link'] = response.request.url
        item['product_name'] =  response.xpath('/html/body/section[1]/h1').extract()
        item['screen'] = response.xpath('/html/body/section[1]/div[3]/div[2]/div[5]/ul/li[1]/div/span[1]').extract()
        item['os'] = response.xpath('/html/body/section[1]/div[3]/div[2]/div[6]/ul/li[2]/div/span').extract()
        item['camera'] = response.xpath('/html/body/section[1]/div[3]/div[2]/div[6]/ul/li[3]/div/span').extract()
        item['front_camera'] = response.xpath('/html/body/section[1]/div[3]/div[2]/div[6]/ul/li[4]/div/span').extract()
        item['chip'] = response.xpath('/html/body/section[1]/div[3]/div[2]/div[6]/ul/li[5]/div/span').extract()

        price = response.xpath('/html/body/section[1]/div[3]/div[2]/div[4]/div[1]/div[1]/p[3]').extract()

        if (not price):
            price = response.xpath('/html/body/section[1]/div[3]/div[2]/div[3]/div[2]/div/p[1]').extract()
        if (not price):
            price = response.xpath('/html/body/section[1]/div[3]/div[2]/div[4]/div[1]/div[1]/strong').extract()
        if (not price):
            price = response.xpath('/html/body/section[7]/div/div[1]/b/b').extract()
        if (not price):
            price = response.xpath('/html/body/section[1]/div[3]/div[2]/div[3]/div[1]/div[1]/strong').extract()
        if (not price):
            price = response.css('.box-price-present').extract()
            
        item['price'] = price
        yield item
