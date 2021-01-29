from flask import Flask, render_template, session, redirect, url_for, request
from functools import wraps
from user.models import User
from bson.objectid import ObjectId
import pymongo
import json


app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = "wsdfghhg345678khghjnmb"
#json_object = json.dumps(serializable_object)

#Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/signup', methods=['POST'])
def signup(): 
    return User.signup()

@app.route('/user/signout')
def signout():
    return User.signout()

#@app.route('/user/delete')
#def signout():
#    return User.delete()

#@app.route('/user/adduserinfo/<id>', methods=['POST'])
#def adduserinfo(id):
    #id = request.form.get("_id")
    #db.users

@app.route('/user/adduserinfo')
def adduserinfo():
    return render_template('addinfo.html')
    #return User.adduserinfo()

@app.route('/user/login', methods=['POST'])
def login():
    return User.login()

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)   