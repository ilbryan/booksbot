# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["thomsonlocal.com"]
    start_urls = [
        'https://www.thomsonlocal.com/search/massage/london',
    ]

    def parse(self, response):
        for book_url in response.css("li.listing > ul > .infoLink > div > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        product = response.css("div.branchDetails")
        item["title"] = product.css("h1.listingName ::text").extract_first()
        item["phone"] = product.css("li.phoneNumber > div > p ::text").extract_first()
        item["web"] = product.css("a.webpageButton ::attr(href)").extract_first()
        item["where"] = product.css('.address > span ::text').getall()
        item['category'] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        ).extract_first()
        item['description'] = response.xpath(
            "//div[@id='product_description']/following-sibling::p/text()"
        ).extract_first()
        item['price'] = response.css('p.price_color ::text').extract_first()
        yield item
