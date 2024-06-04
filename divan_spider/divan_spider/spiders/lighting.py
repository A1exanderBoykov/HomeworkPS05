import scrapy


class LightingSpider(scrapy.Spider):
    name = "lighting"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://divan.ru"]

    def parse(self, response):
        for product in response.css('.product-card'):
            yield {
                'name': product.css('.product-card__name::text').get().strip(),
                'price': product.css('.product-card__price::text').get().strip(),
                'link': response.urljoin(product.css('a::attr(href)').get())
            }

        # Pagination handling
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)