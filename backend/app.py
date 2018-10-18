from flask import Flask,request,jsonify,session,redirect,current_app
from flask_cors import CORS
from Model import Users
from ext import db
from config import config
import pymysql
app = Flask(__name__)
app.config.from_object(config)
CORS(app)
db.init_app(app)

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
#   db.create_all()
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")


    user = Users(username,password,email)
    if Users.query.filter_by(username=username).first():
        return jsonify({'username':username,'password':password,'tips':'Reppeat of username!','flag': '-2'})
    elif Users.query.filter_by(email=email).first():
        return jsonify({'username': username, 'password': password,'tips':"This email has signed!",'flag': '-3'})

    db.session.add(user)
    db.session.commit()
    session['username'] = username
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

@app.route('/api/v1/login',methods=['GET','POST'])
def login():

    username = request.json.get("username")
    password = request.json.get("password")
    user = Users.query.filter_by(username=username).first()
    if user:
        if password != user.password:
            return jsonify({'username': username, 'tips':'Wrong password!','flag':-1})
        session['username'] = username
        return jsonify({'tips': 'Welcome!'+username,'flag':1}),202
    return jsonify({'tips': 'This username doesn\'s registed!','flag':-1})

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
def resource():
    username = request.json.get('username')
    if 'username' in session and username == session.get('username'):
        print(1)
        return jsonify({'data': 'hello! '+username})
    return jsonify({'data':'you are not log in!'})

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

@app.route('/api/v1/logout')
def logout():
    username = request.args.get('username')
    print(username)
    print(session)
    session.pop('username',None)
    return jsonify({'data':username+' log out'})
if __name__ == '__main__':
    app.run(host='0.0.0.0')
