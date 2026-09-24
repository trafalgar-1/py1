import re
from datetime import datetime

class BaseEntity:
    def __init__(self, id_):
        self.id = id_

class Client(BaseEntity):
    def __init__(self, id_, name, email, phone, city):
        super().__init__(id_)
        self.name = name
        self.email = email
        self.phone = phone
        self.city = city

    @staticmethod
    def validate_email(email):
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+\$', email))

    @staticmethod
    def validate_phone(phone):
        return bool(re.match(r'^\+?\d{10,15}\$', phone))

class Product(BaseEntity):
    def __init__(self, id_, name, price):
        super().__init__(id_)
        self.name = name
        self.price = price

class Order(BaseEntity):
    def __init__(self, id_, client_id, product_ids, date):
        super().__init__(id_)
        self.client_id = client_id
        self.product_ids = product_ids
        self.date = date

    def total_cost(self, products):
        return sum(products[pid].price for pid in self.product_ids if pid in products)

