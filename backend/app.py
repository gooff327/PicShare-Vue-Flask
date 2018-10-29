from flask import Flask,request,jsonify,redirect,current_app,g,json
from flask_cors import CORS
from ext import db
from config import config
from Model import *
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
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
    #db.create_all()
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    print(email)
    if Users.query.filter_by(username=username).first():
        return jsonify({'username':username,'password':password,'tips':'Reppeat of username!','err_code': 402})
    elif Users.query.filter_by(email=email).first():
        return jsonify({'username': username, 'password': password,'tips':"This email has signed!",'err_code': 403})
    user = Users(username, email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': username,'password':password,'tips':'Okay,you can sign in now!','err_code': 200})

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
    print(username_or_token,password)
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
# @app.route('/api/v1/mypassages',methods=['GET','POST'])
# @auth.login_required
# def getMydata():
#     datas = []
#     passages = Resource.query.filter_by(author=g.user.username)
#     for passage in passages:
#         datas.append((passage.to_json))
#     return jsonify(datas)

@app.route('/api/v1/resource',methods=['GET','POST'])
@auth.login_required
def resource():
    datas = []
    passages = Resource.query.all()
    for passage in passages:
        datas.append(passage.to_json())
    print(datas)
    return jsonify(datas)
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

@app.route('/api/v1/admin',methods=['GET','POST'])
@auth.login_required
def admin():
    print(request.json)
    db.create_all()
    title = request.json.get('title')
    cls = request.json.get('cls')
    img = request.json.get('img')
    content = request.json.get('content')
    author = g.user.username
    date = datetime.now().isoformat()
    pv = 0
    print(date)
    passage = Resource(title,cls,img,content,pv,author,date)
    db.session.add(passage)
    db.session.commit()
    return jsonify({'tips': 'Admin will check the content you submit!'})




@app.route('/api/v1/logout')
@auth.login_required
def logout():
    username = request.args.get('username')
    print(username)
    return jsonify({'data':username+' log out'})
if __name__ == '__main__':
    app.run(host='0.0.0.0')
