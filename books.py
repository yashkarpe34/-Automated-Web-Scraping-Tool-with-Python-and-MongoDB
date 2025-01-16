import scrapy
from scrapy.spiders import Spider
from pymongo import MongoClient
import datetime
import logging

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = [
        'https://books.toscrape.com/catalogue/category/books/travel_2/index.html',
        'https://books.toscrape.com/catalogue/category/books/romance_8/index.html',
        'https://books.toscrape.com/catalogue/category/books/music_14/index.html'
    ]

    def parse(self, response):
        cards = response.css(".product_pod")
        base_url = 'https://books.toscrape.com/'

        for card in cards:
            title = card.css("h3 > a::attr(title)").get()
            rating = card.css(".star-rating::attr(class)").get().split(" ")[1]
            image_relative_url = card.css("div.image_container img::attr(src)").get()
            image_url = base_url + image_relative_url
            price = card.css(".price_color::text").get()
            availability = card.css(".availability").css("p::text").get().strip()
            inStock = availability == 'In stock'

            logging.info(f"Scraped: Title={title}, Rating={rating}, Image={image_url}, Price={price}, InStock={inStock}")

            page = response.url.split("/")[-2]
            self.insertToDb(page, title, rating, image_url, price, inStock)

    def insertToDb(self, page, title, rating, image, price, inStock):
        client = MongoClient("mongodb+srv://testy:yash9213@cluster0.bouihwi.mongodb.net/")
        db = client.scrapy
        collection = db[page]
        doc = {
            "title": title,
            "rating": rating,
            "image": image,
            "price": price,
            "inStock": inStock,
            "date": datetime.datetime.now(tz=datetime.timezone.utc)
        }
        inserted = collection.insert_one(doc)
        return inserted.inserted_id

class BookDetailsSpider(scrapy.Spider):
    name = 'book_details'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        client = MongoClient("mongodb+srv://testy:yash9213@cluster0.bouihwi.mongodb.net/")
        db = client.scrapy
        collection_names = db.list_collection_names()
        for collection_name in collection_names:
            yield scrapy.Request(url=f'https://books.toscrape.com/catalogue/category/books/{collection_name}/index.html', callback=self.parse)

    def parse(self, response):
        category = response.url.split("/")[-2]
        books = response.css(".product_pod")
        for book in books:
            title = book.css("h3 > a::attr(title)").get()
            link = response.urljoin(book.css("h3 > a::attr(href)").get())
            yield {
                "category": category,
                "title": title,
                "link": link
            }
