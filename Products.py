class Product():

    def __init__(self):

        self.__bean_bag = 501
        self.__wooden_table = 500
        self.__coffee_table = 500

    def get_bean_bag(self):
        return self.__bean_bag

    def get_wooden_table(self):
        return self.__wooden_table

    def get_coffee_table(self):
        return self.__coffee_table


    def set_bean_bag(self, bean_bag):
        self.__bean_bag = bean_bag

    def set_wooden_table(self, wooden_table):
        self.__wooden_table= wooden_table

    def set_coffee_table(self, coffee_table):
        self.__coffee_table = coffee_table

