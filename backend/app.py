from flask import Flask,request,jsonify,redirect,current_app,g,json
from flask_cors import CORS
from Model import Users
from ext import db
from config import config
from Model import *
from flask_httpauth import HTTPBasicAuth
import pymysql
app = Flask(__name__)
app.config.from_object(config)
CORS(app)
db.init_app(app)
auth = HTTPBasicAuth()

"""
Api to sign in
content:application/json
input:
{
    "username":"username",
    "password":"password",
    "email":"email"
}
output:{
    'username':username,
    'password':password,
    'tips':'status in string'
}
"""
@app.route('/api/v1/register',methods=['GET','POST'])
def register():
    '''can remove the '#' to create the user table ! '''
    db.create_all()
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    if Users.query.filter_by(username=username).first():
        return jsonify({'username':username,'password':password,'tips':'Reppeat of username!','flag': '-2'})
    elif Users.query.filter_by(email=email).first():
        return jsonify({'username': username, 'password': password,'tips':"This email has signed!",'flag': '-3'})
    user = Users(username, email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': username,'password':password,'tips':'Okay,you can sign in now!','flag': '2'})

"""
Api to login
content:application/json
input:
{
    "username":"username",
    "password":"password"
}

output:
{
    'username':username,
    'data':'string tips'
}
"""

@auth.verify_password
def verify_password(username_or_token,password):
    print(auth.username())
    if request.path == '/api/v1/login':
        user = Users.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    else:
        user = Users.verify_token(username_or_token)
        if not user:
            return False
    g.user = user
    return True


@app.route('/api/v1/login',methods=['GET','POST'])
@auth.login_required
# def login():
    # username = request.json.get("username")
    # password = request.json.get("password")
    # user = Users.query.filter_by(username=username).first()
    # if user:
    #     if password != user.password:
    #         return jsonify({'username': username, 'tips':'Wrong password!','flag':-1})
    #     return jsonify({'tips': 'Welcome!'+username,'flag':1}),202
    # return jsonify({'tips': 'This username doesn\'s registed!','flag':-1})
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
'''
Api to get resource
Content-Type:application/json
input:
{
    "username":"xxx",
    ...
}
'''

@app.route('/api/v1/resource',methods=['GET','POST'])
@auth.login_required
def resource():
    return jsonify({'tips':'Hello, %s'%g.user.username})
'''
Api to logout
input:
http:XXX/api/v1/logout?username=xxx
to log out xxx even you dont login

output:
{
    'data': xxx log out
}
'''

@app.route('/api/v1/admin')
@auth.login_required
def admin():
    if g.user.username != 'admin':
        return jsonify({'tips':'This page only can be entered by administor!'})


@app.route('/api/v1/logout')
@auth.login_required
def logout():
    username = request.args.get('username')
    print(username)
    return jsonify({'data':username+' log out'})
if __name__ == '__main__':
    app.run(host='0.0.0.0')
