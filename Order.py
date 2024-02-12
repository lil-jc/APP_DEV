class Order:
    order_id = 10000
    def __init__(self, name, address, email, phone, card_number, expiry_date, cvv):
        Order.order_id += 1
        self.__order_id = Order.order_id
        self.__name = name
        self.__address = address
        self.__email = email
        self.__phone = phone
        self.__card_number = card_number
        self.__expiry_date = expiry_date
        self.__cvv = cvv

    def get_order_id(self):
        return self.__order_id
    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    def set_email(self, email):
        self.__email = email

    def set_phone(self, phone):
        self.__phone = phone

    def set_card_number(self, card_number):
        self.__card_number = card_number

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def set_cvv(self, cvv):
        self.__cvv = cvv

    # Getter methods
    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_card_number(self):
        return self.__card_number

    def get_expiry_date(self):
        return self.__expiry_date

    def get_cvv(self):
        return self.__cvv

