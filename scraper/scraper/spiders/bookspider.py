# import scrapy


# class BookspiderSpider(scrapy.Spider):
#     name = "bookspider"
#     allowed_domains = ["books.toscrape.com"]
#     start_urls = ["https://books.toscrape.com"]
    
    

#     def parse(self, response):
#         books = response.css("article.product_pod")
        
#         for book in books:
#             yield {
#                 "title": book.css("h3 > a::text").extract_first(),
#                 "price": book.css("p.price_color::text").extract_first(),
#                 "url": book.css("h3 > a::attr(href)").extract_first(),
#             }
        
#         next_page = response.css("li.next > a::attr(href)").get()
#         if next_page is not None:
#             next_page_url = 'https://books.toscrape.com/' + next_page
#             yield response.follow(next_page_url, callback=self.parse)
            
# import scrapy


# class BookspiderSpider(scrapy.Spider):
#     name = "bookspider"
#     allowed_domains = ["books.toscrape.com"]
#     start_urls = ["https://books.toscrape.com"]

#     def parse(self, response):
#         books = response.css("article.product_pod")

#         for book in books:
#             relative_book_url = book.css("h3 > a::attr(href)").get()
            
#             if 'catalogue/' in relative_book_url:
#                 book_url = response.urljoin(relative_book_url)
#             else:
#                 book_url = response.urljoin("catalogue/" + relative_book_url)
            
#             yield response.follow(book_url, callback=self.parse_book)
            
            

#         # Navigasi ke halaman berikutnya
#         next_page = response.css("li.next > a::attr(href)").get()
#         if next_page:
#             yield response.follow(next_page, callback=self.parse)

        
#         # for page in range(2, 51):
#         #     next_page = f"https://books.toscrape.com/catalogue/page-{page}.html"
#         #     print(next_page)
#         #     yield scrapy.Request(next_page, callback=self.parse)
        
#     def parse_book(self, response):
#         yield {
#             "title": response.css("h1.product_title::text").get(),
#             "price": response.css("p.price_color::text").get(),
#             "url": response.url,
#         }
        
import scrapy
import re


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            relative_book_url = book.css("h3 > a::attr(href)").get()
            
            # Menggunakan response.urljoin untuk menangani URL relatif dan absolut
            book_url = response.urljoin(relative_book_url)
            
            yield response.follow(book_url, callback=self.parse_book)  # Follow URL buku dan panggil parse_book

        # Navigasi ke halaman berikutnya
        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        stock_value = response.xpath('//table[1]/tr[6]/td/text()')
        # stock_value = [int(num) for num in re.findall(r'\((\d+)', stock_value.get())]
        yield {
            # "title": response.css("h1::text").get(),
            # "category": response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get(),
            # "price": response.css("p.price_color::text").get(),
            # "description": response.css("article.product_page > p::text").get(),
            # "url": response.url,
            
            # extract from table
            
            
            
            "UPC": response.xpath('//table[1]/tr[1]/td/text()').get(),
            "Product Type": response.xpath('//table[1]/tr[2]/td/text()').get(),
            "Stock": stock_value.get(),
        }


        
        