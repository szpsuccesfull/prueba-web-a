

from flask import Flask, render_template,request,redirect,url_for,session # For flask implementation    
from bson import ObjectId
from flask.helpers import flash # For ObjectId to work    
from passlib.hash import sha256_crypt
from pymongo import MongoClient
from functools import wraps    
import os    
from pymongo.collation import CollationAlternate

    
app = Flask(__name__) 
app.secret_key ="abcd1234"   
# title = "TODO sample application with Flask and MongoDB"    
# heading = "TODO Reminder with Flask and MongoDB"    
    
client = MongoClient("mongodb://127.0.0.1:27017") #host uri    
db = client.rentaland   #Select the database    
collection = db.Users
collectionApart = db.apartments
#Select the collection name    
    
# def redirect_url():    
#     return request.args.get('next') 
#     request.referrer   
#     url_for('index')    
  
# @app.route("/list")    
# def lists ():    
#     #Display the all Tasks    
#     collection_l = collection.find()    
#     a1="active"    
#     return render_template('index.html',a1=a1,collection=collection_l,t=title,h=heading) 

# @app.route('/layout')
# def layout():
#     return render_template('layout.html')  

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/administracion')
def administracion():
    username = session["Users"]
    user = collection.find_one({'username': username})
    if 'Users' in session:
        return render_template("administracion.html",  user = user["_id"])  
    else:
        return render_template("index.html")

    
@app.route('/')    
def home ():    
    return render_template('home.html')   
     
  

@app.route("/registerB", methods=['POST'])    
def registerB():    
    #Adding a Task 
    if request.method == 'POST':
        fullname=request.form.get("fullname")    
        email=request.form.get("email")    
        username=request.form.get("username")    
        country=request.form.get("country")    
        city=request.form.get("city")    
        password=request.form.get("password")    
        typeUsers=request.form.get("typeUsers")    
        collection.insert({"fullname":fullname, "email":email, "username":username, "country":country, "city":city, "password":password,"typeUsers":typeUsers})
        flash("usuario agregado")
        return redirect(url_for('login'))
    return render_template('register.html') 

@app.route("/loginA", methods=['POST'])    
def loginA():    
    #Adding a Task 
    username = request.form.get('username')
    password = request.form.get('password')
    resultRequest = {'password': password,'username':username}
    session['Users'] = username
    result = collection.find_one(resultRequest)
    if result != None:
            if result["typeUsers"] == "invitado":
                return redirect(url_for('home'))
            else:
                return redirect(url_for('administracion'))   
    

@app.route("/edit_user/<id>")    
def edit_user(id): 
    userEd = collection.find_one({'_id': ObjectId(id)})
    result = []
    result.append({
        '_id':userEd['_id'],
        'fullname':userEd['fullname'],
        'email':userEd['email'],
        'username':userEd['username'],
        'country':userEd['country'],
        'city':userEd['city'],
        'password':userEd['password'],
        'typeUsers':userEd['typeUsers']
    })
    return render_template("edit_user.html", user = result)

@app.route('/edit_save_db/<id>', methods=['POST'])    
def edit_save_db(id):
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    username = request.form.get("username")
    country = request.form.get("country")
    city = request.form.get("city")
    password = request.form.get("password")
    typeUsers = request.form.get("typeUsers")
    collection.update_one({'_id':ObjectId(id)},{"$set":{
        'fullname':fullname,
        'email':email,
        'username':username, 
        'country':country,
        'city':city,
        'password':password,
        'typeUsers':typeUsers
    }})
    return redirect(url_for('home'))

@app.route('/deleteP/<id>',methods=['GET'])
def deleteP(id):
        propertyCollection.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('getProperty'))

<a href="/deleteP/{{property._id}}" class="btn btn-danger btn-delete">Eliminar</a>

const btnDeleteP = document.querySelectorAll('.btn-delete');

   if(btnDeleteP){
      const btnDelete =Array.from(btnDeleteP);
      btnDelete.forEach((btn) =>{
         btn.addEventListener('click', (e) => {
            if(!confirm('Esta seguro que desea eliminar la propiedad?')){
               e.preventDefault();
            }
         });
      });
   }



# @app.route('/delete_apartment/<string:id>' , methods=['POST'])   
# # @is_logged_in 
# def delete_apartment(id):  
#     #Deleting a Task with various references    
#     key=request.values.get("_id")    
#     collection.remove({"_id":ObjectId(key)})    
#     return redirect("/")    
  
# @app.route("/update")    
# def update ():    
#     id=request.values.get("_id")    
#     task=collection.find({"_id":ObjectId(id)})    
#     return render_template('update.html',tasks=task,h=heading,t=title)    
  
# @app.route("/action3", methods=['POST'])    
# def action3 ():    
#     #Updating a Task with various references    
#     name=request.values.get("name")    
#     desc=request.values.get("desc")    
#     date=request.values.get("date")    
#     pr=request.values.get("pr")    
#     id=request.values.get("_id")    
#     collection.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})    
#     return redirect("/")    
  
# @app.route("/search", methods=['GET'])    
# def search():    
#     #Searching a Task with various references    
    
#     key=request.values.get("key")    
#     refer=request.values.get("refer")    
#     if(key=="_id"):    
#         collection_l = collection.find({refer:ObjectId(key)})    
#     else:    
#         collection_l = collection.find({refer:key})    
#     return render_template('searchlist.html',collection=collection_l,t=title,h=heading)    


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))



    
if __name__ == "__main__":    
    app.run(debug=True)   