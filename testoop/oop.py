from fastapi import FastAPI, Body,Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
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
        return None    
            
    def search_cost_by_menu_id(self,menu_id):
        for menu in self.__all_menus:
            if menu.get_menu_id() == menu_id:
                cost = menu.get_cost()
                return cost
        return None    
            
    
    def search_user_by_menu_id(self, menu_id):
        for menu in self.__all_menus:
            if menu.get_menu_id() == menu_id:
                owner = menu.get_owner()
                return owner
        return None

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
    



class Notification:
    def __init__(self, notification_id, account_name,topic, message):
        self.__notification_id = notification_id
        self.__account_name= account_name
        self.__topic = topic
        self.__message = message





class Transaction:
    def __init__(self, transaction_id, account_from, account_to, amount, status): 
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
        if account_from == account_to:
            return {"message": "You can not transfer money to yourself"}
        if account_from.get_balance() < amount:
            return {"message": "Insufficient funds"}
        else:
            account_from.decrease_balance(amount)
            account_to.increase_balance(amount)
            
            system.add_transaction(Transaction(system._System__transaction_id, account_from.get_username(), account_to.get_username(), amount, "Success"))
            system.add_notification(Notification(system._System__notification_id, account_from.get_username(), "Money transfer", f"Transfer {amount} Bath to {account_to.get_username()}"))
            system.add_notification(Notification(system._System__notification_id, account_to.get_username(), "Money received", f"Received {amount} Bath from {account_from.get_username()}"))
            
            return {"message": "Transfer successful"}
        



class Donation(Payment):
    pass

class Cart:
    def __init__(self):
        self.__list_of_order = []  

    def append_order(self, order):
        self.__list_of_order.append(order)
        return {"message":"Add order sucessage"}
        

    def get_list_of_order(self):
        
        return [order.get_order_details() for order in self.__list_of_order]
    
    def get_menu_id(self):
        return [order.get_menu_id() for order in self.__list_of_order]
    
    def get_total_price(self):
        return [order.get_total_price() for order in self.__list_of_order]
    
    def delete_order(self, order):
        for existing_order in self.__list_of_order:
            if existing_order.get_menu_id() == order.get_menu_id():
                self.__list_of_order.remove(existing_order)
                return {"message": "Delete order successful"}
        return {"message": "Order not found"}


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
system.add_menu(
        "ไข่หวานต้มหอมญี่ปุ่น", "admin", "ตั้งกระทะเทฟลอนโดยใช้ไฟอ่อน ๆ นำน้ำมันพืชเช็ดให้ทั่วกระทะ พอกระทะร้อน ยกกระทะขึ้นจากเตา จากนั้นตักไข่ใส่ลงไปพอให้ไข่เคลือบเป็นแผ่นบาง ๆ ทั่วกระทะเมื่อไข่เริ่มเซตตัวดีใช้พายปาดขอบด้านข้าง ค่อย ๆ ม้วนไข่หวานจนเกือบสุดขอบกระทะ จากนั้นใช้พายช่วยประคองไข่ม้วน ให้ถอยหลังมาจุดเริ่มต้นเช็ดกระทะด้วยน้ำมันอีกครั้งให้กระทะสะอาด ตักไข่ใส่ลงไป รอไข่เซตตัวแล้วม้วนต่อจนจบ ทำซ้ำจนไข่หมดหรือได้ความหนาตามต้องการเมื่อไข่หวานได้ความหนาตามต้องการแล้ว ตะแคงกระทะไปมาให้ครบทุกด้านเพื่อจัดทรงให้เป็นชิ้นสี่เหลี่ยม และให้เนื้อไข่หวานแน่นดี",
        "มาอัปเกรดเมนูไข่หวานให้ดีต่อสุขภาพ กับเมนู “ไข่หวานต้นหอมญี่ปุ่น” ที่แฝงต้นหอมหวานกรอบไว้ในเนื้อไข่ม้วนนุ่มฟู เด็ก ๆ ที่ไม่ชอบกินผักยังเทใจให้เลยค่ะ โดยวันนี้เราเลือกใช้ aro ต้นหอมญี่ปุ่นอินทรีย์ ที่ให้โปรตีนสูง พร้อมอุดมไปด้วยวิตามินและสารอาหารหลากหลายชนิด เป็นการเพิ่มประโยชน์ในมื้ออาหารแบบง่าย ๆ ใคร ๆ ก็ทำเองได้ที่บ้านแน่นอนค่ะ ถ้าทุกคนพร้อมกันแล้ว มาจดสูตรไข่หวานต้นหอมญี่ปุ่นกันเลยดีกว่า! มาอัปเกรดเมนูไข่หวานให้ดีต่อสุขภาพ กับเมนู “ไข่หวานต้นหอมญี่ปุ่น” ที่แฝงต้นหอมหวานกรอบไว้ในเนื้อไข่ม้วนนุ่มฟู เด็ก ๆ ที่ไม่ชอบกินผักยังเทใจให้เลยค่ะ โดยวันนี้เราเลือกใช้ aro ต้นหอมญี่ปุ่นอินทรีย์ ที่ให้โปรตีนสูง พร้อมอุดมไปด้วยวิตามินและสารอาหารหลากหลายชนิด เป็นการเพิ่มประโยชน์ในมื้ออาหารแบบง่าย ๆ ใคร ๆ ก็ทำเองได้ที่บ้านแน่นอนค่ะ ถ้าทุกคนพร้อมกันแล้ว มาจดสูตรไข่หวานต้นหอมญี่ปุ่นกันเลยดีกว่า!  ",
        "aro ต้นหอมญี่ปุ่นอินทรีย์ 200 กรัม ไข่ไก่ 6 ฟอง โชยุ 1 ช้อนโต๊ะ  มิริน 1 ช้อนโต๊ะ น้ำตาล 1 ช้อนโต๊ะ น้ำสะอาด 50 กรัม",
        '10 นาที', "20 นาที", "3 คน",
        "260 Kcal/เสิร์ฟ ", 50, True
    )
system.add_menu(
        "Mango Coconut Smoothie ", "admin", "ใส่เนื้อมะม่วงแช่แข็ง เนื้อมะพร้าว กะทิ เกลือ น้ำแข็ง ลงในโหลปั่น จากนั้นใส่ ไซรัปSenoritaกลิ่นมะม่วงอกร่องทองแล้วปั่นให้เข้ากัน อ่านต่อได้ที่ทใส่แก้วตามชอบตกแต่งด้วยเนื้อมะม่วงสุก เนื้อมะพร้าว ราดกะทิ ปิดท้ายด้วยสะระแหน่ แค่นี้ก็พร้อมเสิร์ฟแล้ว อ่านต่อได้ที่ ",
        "ร้อนใจจะขาด ต้องการเครื่องดื่มเย็น ๆ สักแก้วดับกระหายเพิ่มพลังชีวิต! ตอนนี้ใครที่มีอาการเดียวกับน้องหลุมดำ มาค่ะมา! จะพาเข้าครัวไปทำน้ำปั่นกัน ร้อน ๆ แบบนี้จัดไปกับ “Mango Coconut Smoothie” มะม่วงสมูทตี้เนื้อเนียน หอม หวานกลมกล่อม หอมกลิ่นมะม่วงอกร่องด้วย “ไซรัป Senorita กลิ่นมะม่วงอกร่องทอง” เพิ่มความละมุนด้วยเนื้อมะพร้าวเน้น ๆ พร้อมตกแต่งด้วยเนื้อมะม่วงฉ่ำ ๆ ใครได้ลองก็ต้องขอเบิลแก้วที่สองแน่นอน ถ้าพร้อมแล้วมาจดสูตรค่า",
        "ไซรัป Senorita กลิ่นมะม่วงอกร่องทอง 50 มิลลิลิตร เนื้อมะม่วงแช่แข็ง 300 กรัม เนื้อมะพร้าว 150 กรัม กะทิ 50 มิลลิลิตร เกลือ ½ ช้อนชา สะระแหน่ สำหรับตกแต่ง เนื้อมะม่วงสุก สำหรับตกแต่ง เนื้อมะพร้าว สำหรับตกแต่ง กะทิสำหรับตกแต่ง",
        '10 นาที', "20 นาที", "2 คน",
        "500 Kcal/เสิร์ฟ ", 50, True
    )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class MenuPage(BaseModel):
    name: str
    
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
    
    menu_id:int
      

class Top_up_money(BaseModel):
    
    amount:int    

class AddOrder(BaseModel):
    menu_id:int
    
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
    decoded_menu = urllib.parse.unquote(menu)
    for m in system.get_all_menus():
        if m.get_name() == decoded_menu and m._Menu__checked_by_admin == True:
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
    menu = system.search_menu_by_id(comment.menu_id)
    if menu is not None:
        menu.add_comment(comment.commentmenu)
        return {"message":"comment menu successful"}
    return{"message":"Menu not found "}
@app.post("/payment")
def payment_menu(paymentmenu: PaymentMenu):
    account_from_username = system.get_current_log_in()
    account_to_username = system.search_user_by_menu_id(paymentmenu.menu_id)
    menu = system.search_menu_by_id(paymentmenu.menu_id)
    amount = sum(cart.get_total_price())

    account_from = next((user for user in system.get_all_users() if user.get_username() == account_from_username), None)
    account_to = next((user for user in system.get_all_users() if user.get_username() == account_to_username), None)

    if account_from and account_to:
        cart.delete_order(menu)
        return payment.transfer(account_from, account_to, amount)
    return {"message": "User not found"}
    
    
      

       
        
        



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