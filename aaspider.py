# -*- coding: utf-8 -*-
import scrapy


class AaspiderSpider(scrapy.Spider):
    name = 'aaspider'
    allowed_domains = ['www.ifar.org']
    start_urls = [
                'http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author='
                ]
    
    
    def parse(self, response):
        links_info = response.css('td.g_center_name > a::attr(href)')
        links = links_info.extract()
        href = []
        for url in links:
            href.append("http://www.ifar.org/" + url)

        for i in href:
            yield scrapy.Request(i, callback=self.parse_details) 
            
#            yield response.follow(url = href, callback = self.parse_details)

#        for url in response.css('.catalogue_title > a::attr(href)').extract():
#            url_new = prefix.join(url)
#            yield response.follow(url_new, callback = self.parse_details_dos)
            
    
    def parse_details(self, response):
        
        yield {
            'box_info' : response.css('div#box_2_left ::text').extract()
            }
        new_info = response.css('.catalogue_title > a::attr(href)')
        new_links = new_info.extract()
        href_new = []
        for url_new in new_links:
            href_new.append("http://www.ifar.org/" + url_new)

        for s in href_new:
            yield scrapy.Request(s, callback=self.parse_details_dos)
        
        
#        yield {
#            'name': response.css('td.g_center_name > a::text').extract(),
#            'link': response.css('td.g_center_name > a::attr(href)').extract(),
#            'birth_year': response.css('.g_center_birth_year').extract(),
#            'birth_place': response.css('.g_center_birth_place').extract(),
#            'death_year': response.css('.g_center_death_year').extract(),
#            'death_place': response.css('.g_center_death_place').extract()
#        }
     
    def parse_details_dos(self, response):

        yield {
            'column_names' : response.css('.book_title > dl > dt::text').extract(),
            'content' : response.css('.book_title > dl > dd::text').extract()
        }
        
        