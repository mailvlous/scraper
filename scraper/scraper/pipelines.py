# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class BookscraperPipeline:
#     def process_item(self, item, spider):
        
#         adapter = ItemAdapter(item)
        
#         # price convert to float and remove £
#         price_keys = 'price'
#         for price_key in price_keys:
#             value = adapter.get(price_key)
#             value = value.replace('£', '')
#             adapter[price_key] = float(value)
        
#         # stock value
#         availability_string = adapter.get('stock')
#         split_string_array = availability_string.split('(')
#         if len(split_string_array) < 2:
#             adapter['stock'] = 0
#         else:
#             availability_string = split_string_array[1].split(' ')
#             adapter['stock'] = int(availability_string[0])
        
#         return item


from itemadapter import ItemAdapter

# class BookscraperPipeline:
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)

#         # Price conversion to float and removal of £
#         price = adapter.get('price')
#         if price is None:
#             spider.logger.warning(f"Price not found for item: {item}")
#             adapter['price'] = 0.0  # Set default value if price is missing
#         else:
#             try:
#                 # Ensure price is a string before replacing
#                 if isinstance(price, str):
#                     price = price.replace('£', '').strip()
#                     adapter['price'] = float(price)
#                 else:
#                     spider.logger.error(f"Unexpected price format: {price}")
#                     adapter['price'] = 0.0
#             except ValueError as e:
#                 spider.logger.error(f"Failed to convert price: {price} -> {e}")
#                 adapter['price'] = 0.0

#         # Example stock value processing (uncomment if needed)
#         # availability_string = adapter.get('stock')
#         # if availability_string:
#         #     split_string_array = availability_string.split('(')
#         #     if len(split_string_array) < 2:
#         #         adapter['stock'] = 0
#         #     else:
#         #         availability_string = split_string_array[1].split(' ')
#         #         adapter['stock'] = int(availability_string[0])
#         # else:
#         #     adapter['stock'] = 0  # Default if stock is missing

#         return item


import mysql.connector

class SaveToMySQLPipeline:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='BackSpace',
            database='bookscraper'
        )
        
        self.cursor = self.connection.cursor()
        
                ## Create books table if none exists
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            title text,
            category VARCHAR(255),
            price VARCHAR(255),
            description text,
            url VARCHAR(255),
            upc VARCHAR(255),
            product_type VARCHAR(255),
            stock VARCHAR(255),
            PRIMARY KEY (id)
        )
        """)
        
    def process_item(self, item, spider):

        ## Define insert statement
        self.cursor.execute(""" insert into books (

            title, 
            category,
            price,
            description,
            url, 
            upc, 
            product_type, 
            stock,
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["title"],
            item["category"],
            item["price"],
            str(item["description"][0]),
            item["url"],
            item["upc"],
            item["product_type"],
            item["stock"]
        ))

        # ## Execute insert of data into database
        self.connection.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cursor.close()
        self.connection.close()