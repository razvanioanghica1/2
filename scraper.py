# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
pip install scrapy
scrapy startproject olx_houses
scrapy genspider olx olx.ro

import scrapy
import datetime

today = datetime.date.today().strftime('%Y-%m-%d')

class OlxHousesSpider(scrapy.Spider):
    name = 'olx_houses'
    allowed_domains = ['olx.ro']
    start_urls = ['https://www.olx.ro/imobiliare/case-de-vanzare/oradea/',
    'https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/oradea/']
    
    def parse(self, response):
        for href in response.css('a.detailsLink::attr(href)'):
            yield response.follow(href, self.parse_details)
        for href in  response.css('a.pageNextPrev::attr(href)')[-1:]:
            yield response.follow(href, self.parse)
            
            def parse_details(self, response):
        attrs = {
            'url': response.url, 
            'text': response.css('#textContent>p::text').extract_first().strip(),
            'title': response.css('h1::text').extract_first().strip(), 
            'price': response.css('.price-label > strong::text').extract_first().replace(" ", ""),  
            'date': today, 
            'nr_anunt':  response.css('.offer-titlebox em small::text').re('\d+'), 
            'adaugat_la': response.css('.offer-titlebox em::text').re('Adaugat (de pe telefon) +La (.*),') 
        }
        
         for tr in response.css('.details').xpath('tr/td//tr'):
            title = tr.css('th::text').extract_first()
            value = " ".join(x.strip() for x in tr.xpath('td/strong//text()').extract() if x.strip()!="")
            attrs[title]=value
        yield attrs
        
        scrapy run olx -o houses.csv
