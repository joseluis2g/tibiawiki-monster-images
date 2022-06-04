import re
import scrapy
import urllib.request
from os.path import join, exists, basename

imagesFolderName = 'monster-images'

class TibiaWikiImages(scrapy.Spider):
    name = 'tibia-wiki-images'
    start_urls = ['https://tibia.fandom.com/wiki/List_of_Creatures']

    def parse(self, response):
        images = response.css('.ooui-theme-fandomooui .wikitable > * > tr > td > a > img').extract()
        for image in images:
            src = re.findall(r"<img(.*?)data-src=['\"](.*?)['\"].*?\>", image) or re.findall(r"<img(.*?)src=['\"](.*?)['\"].*?\>", image)
            key = re.findall(r"<img(.*?)data-image-key=['\"](.*?)['\"].*?\>", image) or re.findall(r"<img(.*?)alt=['\"](.*?)['\"].*?\>", image)
            if src and key:
                file = join(imagesFolderName, basename(key[0][1]))
                if not exists(file):
                    urllib.request.urlretrieve(response.urljoin((src[0][1]).replace(" ", "_")).replace('&amp;', '&'), file)
        print("Scrapy Spider Done")