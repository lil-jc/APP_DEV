import shelve

class Product:
    count_id_key = 'product_count'

    # initializer method
    def __init__(self, name, price, colour, description, image):
        self.__product_id = self.generate_product_id()
        self.__name = name
        self.__price = price
        self.__colour = colour
        self.__description = description
        self.__image = image

    @classmethod
    def generate_product_id(cls):
        db = shelve.open('product.db', 'c')
        count = db.get(cls.count_id_key, 0)
        count += 1
        db[cls.count_id_key] = count
        db.close()
        return count

    # accessor methods
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_colour(self):
        return self.__colour

    def get_description(self):
        return self.__description

    def get_image(self):
        return self.__image

    # mutator methods
    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_colour(self, colour):
        self.__colour = colour

    def set_description(self, description):
        self.__description = description

    def set_image(self, image):
        self.__image = image
