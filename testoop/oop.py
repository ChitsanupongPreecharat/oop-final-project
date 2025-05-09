from fastapi import FastAPI, Body,Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

class System:
    def __init__(self):
        self.__all_menus = []
        self.__all_users = []
        self.__tag = []
        self.__all_notification = []
        self.__promotion = []
        self.__transaction = []
        self.__next_menu_id = 1
        self.__next_user_id = 1
        self.__notification_id = 1
        self.__transaction_id =1
        self.__current_log_in = None
        

    def add_user(self, username, password):
        if username == "admin":  
            
            new_admin = Admin(self.__next_user_id, username, password, Transaction(0, 0, 0, 0, ""), 0) 
            self.__all_users.append(new_admin)
            self.__next_user_id += 1
            return {"message": "Admin added successfully", "username": new_admin.get_username()}
        else: 
            new_user = Account(self.__next_user_id, username, password,Transaction(0, 0, 0, 0, ""), 0)
            self.__all_users.append(new_user)
            self.__next_user_id += 1
            return {"message": "User added successfully", "username": new_user.get_username()}
        
    
    def add_menu(self, name, owner, how_to,ingredients ,detail,preparing_time, making_itme, size, calories, cost, checked_by_admin):
        if owner != self.get_current_log_in():
            return {"message": "You are not logged in. Please log in first."}
        else:
            new_menu = Menu(self.__next_menu_id, name, owner, how_to,detail,ingredients, preparing_time, making_itme, size, calories, cost, checked_by_admin)
            self.__all_menus.append(new_menu)
            new_notification = Notification(self.__notification_id, owner, "New menu added", f"New menu {name} added by {owner}")
            self.add_notification(new_notification)
            self.__next_menu_id += 1  
            return {"message": "Menu added successfully", "menu_id": new_menu.get_menu_id()}
            
    def log_in(self,username,password):
        for user in self.__all_users:
            if user.get_username() == username:
                if user.get_password() == password:
                    self.__current_log_in = user.get_username()
                    return {"message": "Login successful"}
                else:
                    return {"message": "Incorrect password"}
        
        return   {"message": "Username not found"}  
            
    def log_out(self):
        if self.__current_log_in is not None:    
            self.__current_log_in = None
            return  {"message": "Log out successful"}     
        else:
            return {"message": "You are already logged out"}   

    def get_current_log_in(self):
        return self.__current_log_in

    def add_tag(self, tag: 'Tag'):
        self.__tag.append(tag)

    def add_transaction(self,transaction:'Transaction'):
        self.__transaction.append(transaction)
        self.__transaction_id += 1

    def get_transaction(self):
        user = system.get_current_log_in()
        
        if not user:
            return {"message": "No user is currently logged in"}

        transaction_list = []
        
        for trans in self.__transaction:
            if trans._Transaction__account_from == user or trans._Transaction__account_to  == user: 
                transaction_list.append({
                    "_Transaction__transaction_id": trans._Transaction__transaction_id,
                    "_Transaction__account_from": trans._Transaction__account_from,
                    "_Transaction__account_to": trans._Transaction__account_to,
                    "_Transaction__amount": trans._Transaction__amount,
                    "_Transaction__status": trans._Transaction__status
                })

        return transaction_list   
        

    def add_notification(self, notification: 'Notification'):
        self.__all_notification.append(notification)
        self.__notification_id += 1

    def add_promotion(self, promotion: 'Promotion'):
        self.__promotion.append(promotion)

    def get_all_menus(self):
        return [menu for menu in self.__all_menus if menu.is_checked_by_admin()]

    def get_all_users(self):
        return self.__all_users

    def search_users(self, username):
        for user in self.__all_users:
            if user.get_username() == username:
                return user.get_username()
        return None

    def search_menu(self, name):
        for menu in self.__all_menus:
            if menu.get_name() == name:
                return menu
        return None
    
    def search_menu_by_id(self, menu_id):
        for menu in self.__all_menus:
            if menu.get_menu_id() == menu_id:
                return menu
            
    def search_cost_by_menu_id(self,menu_id):
        for menu in self.__all_menus:
            if menu.get_menu_id() == menu_id:
                cost = menu.get_cost()
                return cost
    
    def search_user_by_menu_id(self,menu_id):
        for menu in self.__all_menus:
            if menu.get_menu_id() == menu_id:
                username = menu.get_name()
                return username


    def show_notification(self):
        user = system.get_current_log_in()
        
        if not user:
            return {"message": "No user is currently logged in"}

        notifications_list = []
        
        for noti in self.__all_notification:
            if noti._Notification__account_name == user: 
                notifications_list.append({
                    "notification_id": noti._Notification__notification_id,
                    "account_name": noti._Notification__account_name,
                    "topic": noti._Notification__topic,
                    "message": noti._Notification__message
                })

        return notifications_list  



    def show_popular_menu(self):
        popular_menus = [menu for menu in self.__all_menus if menu.get_like() > 5]
        return popular_menus

    def buy_food(self):
        pass

    def donate(self):
        pass

   

    def append_item_to_cart(self):
        pass

    def get_waiting_for_approval_menu(self):
         return [menu for menu in self.__all_menus if menu.is_checked_by_admin()==False]
    
    
class User:
    def __init__(self, user_id, name, password):
        
        self.__user_id = user_id
        self.__name = name
        self.__password = password

    def validate(self, username, password):
        if self.__name == username and self.__password == password:
            return True
        else:
            return False

    # def log_in(self, username, password):
    #     return self.validate(username, password)

    def get_username(self):
        return self.__name
    
    def get_user_id(self):
        return self.__user_id
    
    def get_password(self):
        return self.__password

class Nonmember(User):
    def __init__(self):
        super().__init__(0, "", "")

    def register(self, system: 'System', username, password):
        if system.search_users(username) is not None:
            return False
        else:
            system.add_user(username, password)
            system.log_in(username,password)
            system.add_notification(Notification(system._System__notification_id, username, "register successfully", f"Username {username} register sucessfully"))
            return True

class Account(User):
    def __init__(self, account_id, name, password, transaction: 'Transaction', balance:int):
        super().__init__(account_id, name, password)
        self.__account_id = account_id
        self.__transaction = transaction
        self.__balance = balance

    def get_account_id(self):
        return self.__account_id

    def get_balance(self):
        return self.__balance    
    def get_name(self):
        return super().get_username()
   
    def decrease_balance(self,amount):
        self.__balance -= amount

    def increase_balance(self,amount):
        self.__balance += amount    

class Member(Account):
    pass

class Admin(Account):
    def __init__(self, account_id, name, password, transaction: 'Transaction', balance:int):
        super().__init__(account_id, name, password, transaction, balance)
        
        self.__transaction = transaction
        self.__balance = balance

    def validate_admin(self, username, password):
        if username == "admin" and password == "admin":
            return True
        return False

    def register_admin(self, username, password):
        if self.validate_admin(username, password):
            system.add_user(username, password)
            system.log_in(username,password)
            system.add_notification(Notification(system._System__notification_id, username, "register successfully", f"Usrename {username} register sucessfully"))
            return True
        return False
    
    def get_name(self):
        return super().get_name()
    def get_balance(self):
        return super().get_balance()

class Menu:
    def __init__(self, menu_id, name, owner,how_to,ingredients,detail, preparing_time, making_itme, size, calories, cost, checked_by_admin):
        self.__menu_id = menu_id
        self.__name = name
        self.__owner = owner
        self.__how_to = how_to
        self.__ingredients = ingredients
        self.__detail = detail
        self.__preparing_time = preparing_time
        self.__making_itme = making_itme
        self.__size = size
        self.__calories = calories
        self.__like = 0
        self.__comments = []
        self.__cost = cost
        self.__checked_by_admin = checked_by_admin
        
        

    def get_menu_id(self):
        return self.__menu_id

    def get_like(self):
        return self.__like
    
    def add_like(self):
        self.__like +=1

    def add_comment(self, comment):
        self.__comments.append(comment)

    def get_name(self):
        return self.__name

    def get_owner(self):
        return self.__owner
    
    def is_checked_by_admin(self):
        return self.__checked_by_admin
    
    def get_cost(self):
        return self.__cost
    

class Tag(Menu):
    def __init__(self, tag):
        self.__tag = tag
        self.__list_menu = []

class Comment:
    pass

class Notification:
    def __init__(self, notification_id, account_name,topic, message):
        self.__notification_id = notification_id
        self.__account_name= account_name
        self.__topic = topic
        self.__message = message

    # def add_notification(self, system: 'System'):
    #     system.add_notification(self)
        

class Promotion:
    pass

class PromotionCode(Promotion):
    pass

class PromotionService(Promotion):
    pass

class Transaction:
    def __init__(self, transaction_id, account_from, account_to, amount, status): # status = 'transferred' or 'donate'
        self.__transaction_id = transaction_id
        self.__account_from = account_from
        self.__account_to = account_to
        self.__amount = amount
        self.__status = status

class Payment:
    def __init__(self,account_from,account_to,amount:int):
        self.__account_from = account_from
        self.__account_to = account_to
        self.__amount = amount

    def get_account_form(self):
        return self.__account_form    

    def transfer(self, account_from, account_to, amount: int):
        # ตรวจสอบว่า amount เป็นจำนวนที่ถูกต้อง
        if not isinstance(amount, (int, float)):  # ตรวจสอบว่า amount เป็นตัวเลข
            return {"message": "Invalid transfer amount: Amount must be a number"}
        
        # if amount <= 0:  # ตรวจสอบว่า amount น้อยกว่าหรือเท่ากับ 0
        #     return {"message": "Invalid transfer amount: Amount must be greater than 0"}
        
        # ส่วนของการทำธุรกรรม
        sender = account_from
        receiver = account_to

        if sender == receiver:
            return {"message": "Sender and receiver cannot be the same"}

        if not sender:
            return {"message": "Sender not found"}
        if not receiver:
            return {"message": "Receiver not found"}

        # ตรวจสอบยอดเงินของผู้โอน
        if sender.get_balance() < amount:
            return {"message": "Insufficient balance"}

        # ดำเนินการโอน
        sender.decrease_balance(amount)
        receiver.increase_balance(amount)

        # สร้าง transaction ID และบันทึกธุรกรรม
        transaction_id = system.generate_transaction_id()
        transaction = Transaction(transaction_id, sender.get_username(), receiver.get_username(), amount, "payment")
        system.add_transaction(transaction)

        # การแจ้งเตือน
        notification_id = system.generate_notification_id()
        system.add_notification(Notification(notification_id, sender.get_username(), "Payment successful", f"Payment of {amount} to {receiver.get_username()} was successful"))

        return {"message": "Transfer successful", "transaction_id": transaction_id, "amount": amount}



class Donation(Payment):
    pass

class Cart:
    def __init__(self):
        self.__list_of_order = []  # เก็บรายการออเดอร์ทั้งหมด

    def append_order(self, order):
        self.__list_of_order.append(order)
        return {"message":"Add order sucessage"}
        

    def get_list_of_order(self):
        
        return [order.get_order_details() for order in self.__list_of_order]
    
    def get_menu_id(self):
        return [order.get_menu_id() for order in self.__list_of_order]
    
    def get_total_price(self):
        return [order.get_total_price() for order in self.__list_of_order]


class Order:
    def __init__(self, menu_id, price: int, num: int):
        self.__menu_id = menu_id
        self.__price = price
        self.__num = num

    def get_total_price(self):
        return self.__price * self.__num
        

    def get_order_details(self):

        
        return {
            "menu_id": self.__menu_id,
            "price": self.__price,
            "num": self.__num,
            "total_price": self.get_total_price()
        }
    
    def get_menu_id(self):
        return self.__menu_id
    
        

system = System()
nonmember = Nonmember()
admin = Admin(0, "admin", "admin", Transaction(0, 0, 0, 0, ""), 0)
admin.register_admin("admin", "admin")
notification = Notification(1, 1, "New menu added", "New menu added by admin")
system.log_in('admin','admin')
payment = Payment("","",0)
cart = Cart()
order = Order(0,0,0)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class MenuPage(BaseModel):
    name: str
    # owner: str
    # menu_tag: str
    how_to: str
    ingredients:str
    detail:str
    preparing_time: str
    making_time: str
    size: str
    calories: str
    cost: int
    checked_by_admin: bool = False

class RegisterRequest(BaseModel):
    username: str
    password: str    

class CommentMenu(BaseModel):
    menu_id:int
    commentmenu:str

class PaymentMenu(BaseModel):
    # account_from:str
    account_to:str
    amount:int    

class Top_up_money(BaseModel):
    # account_id:int
    amount:int    

class AddOrder(BaseModel):
    menu_id:int
    # price:int
    num:int    


@app.get("/")
def read_root():
    return {"message": "Hello world!"}

@app.post("/add_menu")
def add_menu(menu: MenuPage = Body(...)):
    if system.get_current_log_in() is None:
        return {"message": "You not log in yet"}
    else:
        owner = system.get_current_log_in()
        return system.add_menu(
        menu.name, owner, menu.how_to,menu.ingredients,menu.detail,
        menu.preparing_time, menu.making_time, menu.size,
        menu.calories, menu.cost, menu.checked_by_admin
    )
    

@app.get("/menus")
def get_all_menus():
    return [menu.__dict__ for menu in system.get_all_menus()]



@app.post("/register")
def register(request: RegisterRequest):
    if admin.register_admin(request.username, request.password):
        
        return {"message": "Admin registered successfully"}
    elif nonmember.register(system, request.username, request.password):
        
        
        return {"message": "User registered successfully"}
    else:
        return {"message": "This username is already taken. Please try a different one."}
    
@app.post("/log_in")   
def log_in(request:RegisterRequest) :
    return system.log_in(request.username,request.password)

@app.get("/log_out")
def log_out():
    return system.log_out()
        

@app.get("/users")
def get_all_users():
    users = [{"username": user.get_username(), "user_id": user.get_user_id(),"user_balance":user.get_balance()} for user in system.get_all_users()]
    return users

@app.post("/top_up")
def top_up(top_up_money:Top_up_money):
    account = system.get_current_log_in()
    for user in system.get_all_users():
        if user.get_username() == account:
            user.increase_balance(top_up_money.amount)
            system.add_notification(Notification(system._System__notification_id, user.get_username(), "Money deposit", f"User {user.get_username()} money deposit {top_up_money.amount} Bath"))
            return {"message":"increase balance sucessful"}
    return {"message":"Uesr not found"}    

@app.get("/searchMenu")
def search_menu(menu:str = Query(...,description="menu to search")):
    for m in system.get_all_menus():
        if m.get_name() == menu and m._Menu__checked_by_admin == True:
            return {"menu":f"menu {m.get_name()} found"}
        
    return {"message":f"menu {menu} not found"}

@app.get("/showMenu")
def search_menu(menu:str = Query(...,description="menu to search")):
    for m in system.get_all_menus():
        if m.get_name() == menu and m._Menu__checked_by_admin == True:
            return {"menu":m}
        
    return {"message":f"menu {menu} not found"}

@app.get("/serach_not_approved_menu")
def get_waiting_for_approval_menu():
    return [menu.__dict__ for menu in system.get_waiting_for_approval_menu()]

@app.post("/approve_menu/{menu_id}")
def approve_menu(menu_id: int):
    user = system.get_current_log_in()
    if user != 'admin':
        return {"message": "You can not approved or reject anything"}
    menu = system.search_menu_by_id(menu_id)
    if menu is None:
        return {"message": "Menu id not found"}
    else:
        menu._Menu__checked_by_admin = True
        system.add_notification(Notification(system._System__notification_id, menu.get_owner(), "Menu approved", f"Menu {menu.get_name()} approved by admin"))
        
        return {"message": "Menu approved"}
    
@app.delete("/delete_menu/{menu_id}")
def delete_menu(menu_id: int):
    menu = system.search_menu_by_id(menu_id)
    if menu is None:
        return {"message": "Menu id not found"}
    else:
        system._System__all_menus.remove(menu)
        system.add_notification(Notification(system._System__notification_id, menu.get_owner(), "Menu dejected", f"Menu {menu.get_name()} dejected by admin"))
        return {"message": "Menu deleted "}    
    

@app.get("/show_notification")
def show_notification():
    return system.show_notification()
    




@app.get("/current_log_in")
def current_log_in():
    # Fetch the current logged-in user
    current_user = next((user for user in system.get_all_users() if user.get_username() == system.get_current_log_in()), None)

    if current_user:
        return [{"username": current_user.get_username(), "user_id": current_user.get_user_id(), "user_balance": current_user.get_balance()}]
    else:
        return []  

   
    



@app.get("/LikeMenu/{menu_id}")
def likemenu(menu_id:int):
    menu = system.search_menu_by_id(menu_id)
    if menu is not None:
        menu.add_like()
        return {"message":"like menu "}
    return{"message":"Menu not found "}

@app.post("/CommentMenu")
def commentmenu(comment:CommentMenu):
    menu = system.search_menu(comment.menu_id)
    if menu is not None:
        menu.add_comment(comment.commentmenu)
        return {"message":"comment menu successful"}
    return{"message":"Menu not found "}
@app.get("/payment")
def payment_menu():
    
    account_from = system.get_current_log_in()

    # ตรวจสอบข้อมูลของ cart
    menu_id = [cart.get_menu_id()]  # ควรจะเป็นลิสต์ของ menu_id
    total_price = [order.get_total_price()]  # ควรจะเป็นลิสต์ของ total_price

    if total_price is None:
        return {"message": "total_price is None"}
    if isinstance(account_from, list):
        return {"message": "Invalid account data"}

    payments = []

    # ควรเริ่มจาก 0 แทนที่จะเป็น 1 เพราะเราอาจจะมีเพียงแค่ 1 รายการใน menu_id และ total_price
    for i in range(len(menu_id)):  # ใช้ len(menu_id) เพื่อหลีกเลี่ยงการเกิด IndexError
        account_to = system.search_user_by_menu_id(menu_id[i])  # ค้นหาผู้รับ
        if isinstance(account_to, list):
            account_to = account_to[0]  # เลือกบัญชีผู้รับแรก
            if account_to is None:
                return {"message": "account_to None"}

        # ตรวจสอบว่า total_price[i] เป็นลิสต์หรือไม่
        if isinstance(total_price[i], list):
            if len(total_price[i]) > 0:
                try:
                    amount = int(total_price[i])  # แปลงจำนวนเงินจากลิสต์
                except ValueError:
                    return {"message": f"Invalid amount value: {total_price[i]} is not a valid number"}
            else:
                return {"message": f"Invalid amount: List is empty at index {i}"}
        else:
            # ถ้าไม่ใช่ลิสต์ ก็ให้พยายามแปลงเป็นจำนวนเต็ม
            try:
                amount = int(total_price[i])
            except ValueError:
                return {"message": f"Invalid amount value: {total_price[i]} is not a valid number"}

        # สร้างการทำธุรกรรมและโอนเงิน
        payment = Payment(account_from, account_to, amount)
        transfer_result = payment.transfer(account_from, account_to, amount)
        payments.append(transfer_result)

    return {"payments": payments}

      

       
        
        



@app.get("/transaction")
def transaction():
    return system.get_transaction()

@app.post("/addOrder")
def add_order(AddOrder:AddOrder):
    menu= system.search_menu_by_id(AddOrder.menu_id)
    price = menu.get_cost()
    order = Order(AddOrder.menu_id,price,AddOrder.num)
    cart.append_order(order)
    return {"message":"Add order sucessage"}

@app.get("/get_cart")
def get_cart():
    return {"cart": cart.get_list_of_order()}