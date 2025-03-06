class System:
    def __init__(self):
        self.__all_menus =[]
        self.__all_users =[]
        self.__tag =[]
        self.__all_notification =[]
        self.__promotion =[]

    def add_user(self,user):
        self.__all_users.append(user)

    def add_menu_to_system(self,menu):
        self.__all_menus.append(menu)  

    def add_tag(self,tag):
        self.__tag.append(tag)

    def add_notification(self,notification):
        self.__all_notification.append(notification)

    def add_promotion(self,promotion):
        self.__promotion.append(promotion)

    def search_users(self,username):
        for user in self.__all_users:
            if user.username == username:
                return user
        return None

    def search_menu(self,name):
        for menu in self.__all_menus:
            if menu.name == name:
                return menu
        return None

    def show_notification(self):
        return self.__all_notification

    def show_popular_menu(self,):
        
        for menu in range(self.__all_menus):
            if menu.get_like() >5:
                return menu 

    def buy_food(self,):
        pass

    def add_menu(self,):
        pass

    def donate(self,):
        pass

    def register(self,):
        pass    

    def append_item_to_cart(self,):
        pass

    def get_waiting_for_approval_emnu(self,):
        pass
    
class User:
    def __init__(self,name,password):
        self.__name = name
        self.__password = password

    def  validate(self,username,password):
        if self.__name == username and self.password == password:
            return True
        else:
            return False 

    
    def log_in(self,username,password):
        if self.validate(self,username,password):
            return True
        else:
            return False

class Nonmember(User):
    def register(self,username,password):
        for user in System.__all_users:
            if user == username:
                return False
            else:
                 System.add_user(self,username,password)    # register

class Account(User):
    pass

class Member(Account):
    pass

class Admin(Account):
    pass

class Menu:
    
    def __init__(self,name,owner,menu_tag,how_to,preparing_time,making_itme,size,calories,cost):
        self.__menu_id = 0
        self.__name = name
        self.__owner = owner
        self.__menu_tag = menu_tag
        self.__how_to = how_to
        self.__preparing_time = preparing_time
        self.__making_itme = making_itme
        self.__size = size
        self.__calories = calories
        self.__confirmed_by_admin = False
        self.__like = 0
        self.__comments = []
        self.__cost = 0

    def add_menu(self,menu):
        self.__menu.append(menu)  #มาทำต่อ ดุตามหน้า ui    

    @property
    def get_like(self):
        return self.__like

class Tag(Menu):
    def __init__(self,tag):
        self.__tag = tag
        self.__list_menu=[]

class Comment:
    pass


class Notification:
    pass


class Promotion:
    pass

class PromotionCode(Promotion):
    pass

class PromotionService(Promotion):
    pass

class Transaction:
    pass

class Payment:
    pass

class Donation(Payment):
    pass

class Cart:
    pass

class Order:
    pass    

