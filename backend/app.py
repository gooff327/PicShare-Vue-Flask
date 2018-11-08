from flask import Flask,request,jsonify,g,json,make_response
from flask_cors import CORS
from ext import db
from config import config
import base64
from Model import *
import os
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from urllib.request import urlopen
app = Flask(__name__)
app.config.from_object(config)
CORS(app)
db.init_app(app)
auth = HTTPBasicAuth()
basedir = os.path.abspath(os.path.dirname(__file__))
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
@app.route('/api/v1/getImage',methods=['GET','POST'])
def getImage():
    username= ((request.form).to_dict()).get('username')
    img = request.files.get('file')
    if img.filename[-3:]=='peg':
        imageName = username+img.filename[-5:]
    else:
        imageName = username+img.filename[-4:]
    path = basedir +"/static/img/avatar"
    filepath = path +imageName
    img.save(filepath)
    # img_name = '1.jpg'
    # if not img and img_name:
    #     return make_response('上传失败！')
    # with open(img_name, 'wb')as f:
    #     f.write(img)
    #     f.close()
    return jsonify({'id':'1'})


@app.route('/api/v1/register',methods=['GET','POST'])
def register():
    '''can remove the '#' to create the user table ! '''
    db.create_all()
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    if Users.query.filter_by(username=username).first():
        return jsonify({'username':username,'password':password,'tips':'Reppeat of username!','err_code': 402})
    elif Users.query.filter_by(email=email).first():
        return jsonify({'username': username, 'password': password,'tips':"This email has signed!",'err_code': 403})
    user = Users(username,email)
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

@app.route('/api/v1/resources',methods=['GET','POST'])
@auth.login_required
def resource():
    datas = {}
    passages = Resource.query.all()
    for passage in passages:
        avatarPath = config.AVATARDIR+passage.uavatar
        with open(avatarPath, 'rb') as f:
            avatar = f.read()
            avatar = str(base64.b64encode(avatar))
            passage.uavatar = avatar[2:-1]
        imgPath = passage.img
        with open(imgPath, 'rb') as f:
            image = f.read()
            image = str(base64.b64encode(image))
            passage.img = image[2:-1]

    for n in range(len(passages)):
        datas[n] = passages[n].to_json()
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
@app.route('/api/v1/admire',methods=['GET','POST'])
@auth.login_required
def admire():
    admire = {}
    if request.method == 'GET':
        if g.user.admire == None:
            passages = db.session.query(Resource.pid).all()
            print(passages)
            for pid in passages:
                admire[pid[0]] = False
            user = Users.query.filter_by(username = g.user.username).first()
            user.admire = json.dumps(admire)
            db.session.commit()
            db.session.close()
            return jsonify({"admire": admire,"tips": "Successed!", "code": 520})
        try:
            data = json.loads(g.user.admire)
            print(data)
            return jsonify({"admire": data,"tips": "Successed!", "code": 520})
        except TypeError:
            return  jsonify({"tips": "Like nothing!", "code": 419})
    if request.method == 'POST':
        print(request)
        user = Users.query.filter_by(username = g.user.username).first()
        data = request.json
        user.admire = json.dumps(data)
        db.session.commit()
        db.session.close()
        return jsonify({"Tips": "Successed!", "code": 520})
@app.route('/api/v1/admin',methods=['GET','POST'])
@auth.login_required
def contentManager():
    print(request.json)
    db.create_all()
    img = request.json.get('img')
    content = request.json.get('content')
    author = g.user.username
    date = datetime.now().isoformat()
    pv = 0
    passage = Resource(img,content,pv,author,date)
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
    app.run()
