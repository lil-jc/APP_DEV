class Donation:
    user_id = 0

    # initializer method
    def __init__(self, name, email, Umessage, service, scheduledate, scheduletime, furnituretype, quantity, fragile, packaged, address, number):
        Donation.user_id += 1
        self.__user_id = Donation.user_id
        self.__name = name
        self.__email = email
        self.__Umessage = Umessage
        self.__service = service
        self.__scheduledate = scheduledate
        self.__scheduletime = scheduletime
        self.__furnituretype= furnituretype
        self.__quantity = quantity
        self.__fragile = fragile
        self.__packaged = packaged
        self.__address = address
        self.__number = number



    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_message(self):
        return self.__Umessage

    def get_service(self):
        return self.__service
    
    def get_scheduledate(self):
        return self.__scheduledate
    
    def get_scheduletime(self):
        return self.__scheduletime

    def get_furnituretype(self):
        return self.__furnituretype
    
    def get_quantity(self):
        return self.__quantity
    
    def get_fragile(self):
        return self.__fragile
    
    def get_packaged(self):
        return self.__packaged

    def get_address(self):
        return self.__address

    def get_number(self):
        return self.__number

    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_message(self, Umessage):
        self.__Umessage = Umessage

    def set_service(self, service):
        self.__service = service
    
    def set_scheduledate(self, scheduledate):
        self.__scheduledate = scheduledate
    
    def set_scheduletime(self, scheduletime):
        self.__scheduletime = scheduletime

    def set_furnituretype(self, furnituretype):
        self.__furnituretype = furnituretype

    def set_quantity(self, quantity):
        self.__quantity = quantity
    
    def set_fragile(self, fragile):
        self.__fragile = fragile
    
    def set_packaged(self, packaged):
        self.__packaged = packaged

    def set_address(self, address):
        self.__address = address

    def set_number(self, number):
        self.__number = number


