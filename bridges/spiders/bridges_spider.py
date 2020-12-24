import scrapy
from bridges import items

class BridgesSpider(scrapy.Spider):
    name = "bridges-spider"

    def start_requests(self):
        urls = [
            'https://structurae.net/en/structures/bridges/masonry-bridges/list?min=0' + str(i * 100)
            for i in range(29)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = '/'.join(response.url.split('/')[:3])
        link_table = response.xpath('//table[@class="mobile-scroll-table"]')
        image_links = link_table.xpath('//a[@class="listableleft"]/@href')
        for sub_url in image_links.getall():
            link = base_url + sub_url + '/media'
            yield scrapy.Request(url=link, callback=self.follow_link)
            
            

    def follow_link(self, response):
        base_url = '/'.join(response.url.split('/')[:3])
        bridge_name = '_'.join(response.xpath('//a[@class="imageThumbLink_2"]//@href').extract_first().split('-')[1:])
        print(bridge_name)
        image_links = response.xpath('//a[@class="imageThumbLink_2"]//@href').extract()
        
        for sub_url in image_links:
            link = base_url + sub_url
            yield scrapy.Request(url=link, callback=self.open_image_link)


    def open_image_link(self, response):

        image_item = items.ImageItem()
        image_item['image_urls'] = response.xpath('//div[@class="mediaItem "]//img//@src').extract()
        bridge_name = response.xpath('//div[@class="mediaItem "]//img//@alt').extract_first()
        image_item['bridge_name'] = '_'.join(bridge_name.lower().strip().split())
        yield image_item