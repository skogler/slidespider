#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy

baseurl = 'http://kti.tugraz.at/staff/denis/courses/netsci/'

class SlideSpider(scrapy.Spider):
    name = 'slidespider'
    num_links = 0
    start_urls = [baseurl]

    visited = set()
    
    def parse(self, response):
        num_links = 0
        for link in response.css('#calender a ::attr(href)').extract():
            if link.endswith('pdf'):
                if link not in self.visited:
                    self.visited.add(link)
                    num_links = num_links + 1
                    yield scrapy.Request(response.urljoin(link), callback=self.savepdf, meta = {'custom_linkindex' : num_links})

    def savepdf(self, response):
        filename = response.url.split('/')[-1]
        filename = '{:02d}_{}'.format(response.meta['custom_linkindex'], filename)
        with open(filename, 'wb') as outf:
            outf.write(response.body)






