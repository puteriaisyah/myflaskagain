from flask import Flask, jsonify, request, session, redirect
import pymongo
from passlib.hash import pbkdf2_sha256
import uuid

client = pymongo.MongoClient("mongodb+srv://usertest:bIirDOL82rPUsVHO@clusters.otuvw.mongodb.net/systemuser?retryWrites=true&w=majority")
db = client.systemuser

class User():

    def start_session(user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user)

    def signup():
        print(request.form)

        #Create the user object
        user = {
             "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        #Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        #Check for existing email address
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "error" : "Email address already exists"})

        if db.users.insert_one(user):
            #return "user"
            return User.start_session(user)
        
        return jsonify({ "error" : "Signup failed"})
    
    def signout():
        session.clear()
        return redirect('/') 

    def login():
        user = db.users.find_one({
            "email": request.form.get('email')
        })
        #if user:
        #    return User.start_session(user)
        #return jsonify({ "error": "Invalid login credentials"})
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return User.start_session(user)
        return jsonify({ "error": "Invalid login credentials"})
    
    def adduserinfo(user):
        #id = request.form.get("_id")
        #db.users.
        #print(request.form)
        #if user:
        #    current_user = user['_id']
        #    return User.start_session(current_user)
        user = {
             "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "age": request.form.get('age'),
            "occupation": request.form.get('occupation'),
            "gender": request.form.get('gender'),
            "email": request.form.get('email'),
            "country": request.form.get('country'),
            "contact": request.form.get('contact')
        }
        if db.users.insert_one(user):
            #return "user"
            return jsonify(user)
        return redirect('/dashboard/')
        
        
