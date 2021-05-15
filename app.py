

from flask import Flask, render_template,request,redirect,url_for,session # For flask implementation    
from bson import ObjectId
from flask.helpers import flash # For ObjectId to work    
from passlib.hash import sha256_crypt
from pymongo import MongoClient
from functools import wraps    
import os    
    
app = Flask(__name__) 
app.secret_key ="abcd1234"   
title = "TODO sample application with Flask and MongoDB"    
heading = "TODO Reminder with Flask and MongoDB"    
    
client = MongoClient("mongodb://127.0.0.1:27017") #host uri    
db = client.rentaland   #Select the database    
collection = db.Users #Select the collection name    
    
def redirect_url():    
    return request.args.get('next') 
    request.referrer   
    url_for('index')    
  
@app.route("/list")    
def lists ():    
    #Display the all Tasks    
    collection_l = collection.find()    
    a1="active"    
    return render_template('index.html',a1=a1,collection=collection_l,t=title,h=heading) 

@app.route('/layout')
def layout():
    return render_template('layout.php')  

@app.route('/administracion')
def administracion():
    # if 'username' in session and  session['typeUsers'] == "anfitrion":
        return render_template("administracion.html") 
    
@app.route("/")    
def home ():    
    # mycursor = collection.find_one('collection')    
    # for document in homie :
    #     if  document.starswith(""):
    #         mycursor.append(document)
    #     print(document)
        return render_template('home.html' )   #iterate=mycursor
  
  
@app.route("/completed")    
def completed ():    
    #Display the Completed Tasks    
    collection_l = collection.find({"done":"yes"})    
    a3="active"    
    return render_template('index.html',a3=a3,collection=collection_l,t=title,h=heading)    
  
# @app.route("/done")    
# def done ():    
#     #Done-or-not ICON    
#     id=request.values.get("_id")    
#     task=collection.find({"_id":ObjectId(id)})    
#     if(task[0]["done"]=="yes"):    
#         collection.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})    
#     else:    
#         collection.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})    
#     redir=redirect_url()        
    
#     return redirect(redir)    
  
@app.route("/register", methods=['GET','POST'])    
def register ():    
    #Adding a Task 
    if request.method == 'POST':
        fullname=request.values.get("fullname")    
        email=request.values.get("email")    
        username=request.values.get("username")    
        country=request.values.get("country")    
        city=request.values.get("city")    
        password=request.values.get("password")    
        typeUsers=request.values.get("typeUsers")    
        collection.insert({ "fullname":fullname, "email":email, "username":username, "country":country, "city":city, "password":password,"typeUsers":typeUsers, "done":"no"})
        flash("usuario agregado")
        # return redirect(url_for('done'))   
    return render_template("register.html")   

@app.route("/login", methods=['GET','POST'])    
def login ():    
    #Adding a Task 
    if request.method == 'POST':
        username=request.values.get("username")        
        password=request.values.get("password")    
        typeUsers=request.values.get("typeUsers")    
        collection.find_one({ "username":username, "password":password,"typeUsers":typeUsers})
        flash("usuario ha sido logeado")
        # return redirect(url_for('done'))  
        return redirect(url_for('administracion'))  
    return render_template("login.html")  

@app.route('/delete_apartment/<string:id>' , methods=['POST'])   
# @is_logged_in 
def delete_apartment(id):  
    #Deleting a Task with various references    
    key=request.values.get("_id")    
    collection.remove({"_id":ObjectId(key)})    
    return redirect("/")    
  
@app.route("/update")    
def update ():    
    id=request.values.get("_id")    
    task=collection.find({"_id":ObjectId(id)})    
    return render_template('update.html',tasks=task,h=heading,t=title)    
  
@app.route("/action3", methods=['POST'])    
def action3 ():    
    #Updating a Task with various references    
    name=request.values.get("name")    
    desc=request.values.get("desc")    
    date=request.values.get("date")    
    pr=request.values.get("pr")    
    id=request.values.get("_id")    
    collection.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})    
    return redirect("/")    
  
@app.route("/search", methods=['GET'])    
def search():    
    #Searching a Task with various references    
    
    key=request.values.get("key")    
    refer=request.values.get("refer")    
    if(key=="_id"):    
        collection_l = collection.find({refer:ObjectId(key)})    
    else:    
        collection_l = collection.find({refer:key})    
    return render_template('searchlist.html',collection=collection_l,t=title,h=heading)    

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
    
if __name__ == "__main__":    
    
    app.run(debug=True)   