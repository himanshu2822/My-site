from flask_restful import Resource, Api
from flask import render_template
from os import system
from flask import *
import pymongo

#Connecting to the  client local/cloud.
#client = pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient("mongodb+srv://himanshu2822:himanshu2822@cluster0.ozsjond.mongodb.net/?retryWrites=true&w=majority")
print(client)

#Creating a collection/datafield
db = client["Himanshu"]  #name of DB
collection = db['User-DB'] # name of collection
collection2 = db['contact-user']
collection3 = db['orders']


dict = [{"name":"Paras","address":"Shimla","number":1234567890,"email":"paras@mail.com","psw":"paras1234"},
        {"name":"Abhay","address":"Solan","number":7987654321,"email":"abhay@mail.com","psw":"abhay1234"},
        {"name":"Aman","address":"Hamirpur","number":7821450359,"email":"aman@mail.com","psw":"aman1234"},
        {"name":"Himanshu","address":"Karsog","number":5671450359,"email":"himanshu@mail.com","psw":"himanshu1234"},
        {"name":"Raghav","address":"Kangra","number":1024598500,"email":"raghav@mail.com","psw":"ragahv1234"}              
] 
collection.insert_many(dict)


system("clear")

#staring web app
app = Flask(__name__)
api = Api(app)

#Main Home Page
class Home(Resource):
  def get(self):
    print("--------------------------")
    print("Home Page loaded") 
    return make_response(render_template('index.html'))

#Login page   
class login(Resource):
  def get(self):
    print("--------------------------")
    print("Login Page loaded") 
    return make_response(render_template('login.html')) 

#After Login Welcome page =) login done.
class welcome(Resource):
  def post(self):
    email = request.form.get('email')
    psw = request.form.get('psw')
    print(email,psw)
    data = collection.find_one({"email":email,"psw":psw},{"_id":0})
    try:
      if email == data['email'] and psw == data['psw']:
        print("--------------------------")
        print(f"Welcome Page for {data['name']} loaded/Login Done")  
        return make_response(render_template('welcome.html',name=data['name'],add=data['address'],num=data['number'],url="url"))
      
    except:  
      print("--------------------------")
      print("Invalid password")
      return make_response(render_template('login.html'))
        
  def get(self):
    print("--------------------------")
    print("Login First")
    return make_response(render_template('login.html'))
  
#Contact us
class contact(Resource):
  def get(self):
    print("--------------------------")
    return make_response(render_template('connect.html')) 
  
#Contact us Done
class ok(Resource):
  def post(self):
    email = request.form.get('email')
    name = request.form.get('name')
    no = request.form.get('no')
    print(email,name,no)
    dict = {"name":name,"email":email,"no":no}
    collection2.insert_one(dict)
    print("--------------------------")
    return (f"Thank You {name}. We will contact you soon.") 
  
# order page
class order(Resource):
  def get(self):
    print("--------------------------")
    return make_response(render_template('order.html')) 
  
#order page done
class order_done(Resource):
  def post(self):
    name = request.form.get('name')
    qty = request.form.get('qty')
    no = request.form.get('no')
    variety = request.form.get('variety')
    add = request.form.get('add')
    
    if variety == "royal":
      tot = 2200*int(qty)
    elif variety == "golden"  :
      tot = 1200*int(qty)
    elif variety == "spur"  :
      tot = 3400*int(qty)
    elif variety == "rgolden"  :
      tot = 1200*int(qty)
    dict = {"name":name,"address":add,"variety":variety,"Qunatity":qty,"contact":no}
    collection3.insert_one(dict)
    print("--------------------------")
    return {"Message":f"order confirmed  for Mr./Ms. {name}","Variety":variety,"Quantity":qty,"Address":add,"Total cost":tot,"NOTE":"You shall be contacted by our agent for your order confirmation"},200

api.add_resource(Home, '/',methods=['GET', 'POST'])
api.add_resource(login, '/login',methods=['GET', 'POST'])
api.add_resource(ok, '/ok',methods=['GET', 'POST'])
api.add_resource(welcome, '/welcome',methods=['GET', 'POST'])
api.add_resource(contact, '/contact',methods=['GET', 'POST'])
api.add_resource(order, '/order',methods=['GET', 'POST'])
api.add_resource(order_done, '/order_done',methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(debug=True)  
    