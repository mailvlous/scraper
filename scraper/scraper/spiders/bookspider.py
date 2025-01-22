import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    
    

    def parse(self, response):
        books = response.css("article.product_pod")
        
        for book in books:
            yield {
                "title": book.css("h3 > a::text").extract_first(),
                "price": book.css("p.price_color::text").extract_first(),
                "url": book.css("h3 > a::attr(href)").extract_first(),
            }
        
        next_page = response.css("li.next > a::attr(href)").extract_first()
        print(next_page)
        