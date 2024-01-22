
class User():
    count_id = 0

    def __init__(self, first_name, last_name, email, password):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password

    def get_user_id(self):
        return self.__user_id
    
    def get_id(self):
        return str(self.__user_id)

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def check_credentials(self, email, password):
        return self.__email == email and self.__password == password
    
    def is_active(self):
        # Assuming all users are considered active. Modify this based on your logic.
        return True
    
    def is_authenticated(self):
        # Assuming all users are authenticated once they are logged in.
        return True
    
    def is_active(self):
        # Implement your logic to determine if the user account is active.
        # For example, return True if the user account is active, and False otherwise.
        return True
    
    def is_anonymous(self):
        # Assuming all users are not anonymous (authenticated users).
        return False

