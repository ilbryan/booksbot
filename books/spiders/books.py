# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["treatwell.co.uk"]
    start_urls = [
        'https://www.treatwell.co.uk/places/treatment-herbal-medicine-and-supplements/offer-type-local/in-london-uk/',
    ]

    def parse(self, response):
        for book_url in response.css("div.Results-module--results--e3b89d > .BrowseResult-module--container--a0806d > div > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("a.Pagination-module--next--740edf ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        product = response.css("div.styles-module--wrapper--0a792c.compose-module--baseWrapper--ff8a8d")
        item["title"] = product.css("h1.Text-module_lgHeader__3Rm3T.style-module--name--9886df ::text").extract_first()
        item["img"] = product.css("div.Carousel-module--wrapper--be7da7 img.ResizingImage-module--image--23a8d7").xpath('@src').getall()
        item["where"] = product.css('.Text-module_xsHeader__1lwdU .style-module--addressPart--484b23 ::text').getall()
        item["open"] = product.css('.styles-module--gridOpeningTimes--2ca6ce > .Stack-module_stack__1yFnE.Stack-module_xs__3fXRh *::text').getall()
        item['category'] = product.css('.Breadcrumbs-module--breadcrumbs--52ce45 *::text').getall()
        yield item
