# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

import os
from urllib.parse import urlparse



class BridgesPipeline:
    def process_item(self, item, spider):
        return item

class BridgeImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return item['bridge_name'] + '/' + os.path.basename(urlparse(request.url).path)