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
@app.route('/api/v1/post/avatar',methods=['GET','POST'])
def get_avatar():
    username= ((request.form).to_dict()).get('username')
    img = request.files.get('file')
    imageName = username+img.filename[-4:]
    path = basedir +"/static/img/avatar/"
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
    if(os.path.exists(basedir+"/static/img/avatar/"+username+".jpg")):
        avatar = username+'.jpg'
    else:
        avatar = username + '.png'
    user = Users(username,email,avatar)
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
    user = {}
    token = g.user.generate_auth_token()
    print(g.user.username)
    avatarPath = config.AVATARDIR + g.user.avatar
    user['username'] = g.user.username
    user['uid'] = g.user.uid
    user['avatar'] = sendImage(avatarPath)
    return jsonify({'token': token.decode('ascii'),'user': user})
'''
Api to get resource
Content-Type:application/json
input:
{
    "username":"xxx",
    ...
}
'''


@app.route('/api/v1/resources',methods=['GET','POST'])
@auth.login_required
def resource():
    db.create_all()
    datas = {}
    passages = Resource.query.all()
    for passage in passages:
        avatarPath = config.AVATARDIR+passage.uavatar
        passage.uavatar = sendImage(avatarPath)
        imgPath = passage.img
        passage.img = sendImage(imgPath)

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
    print(g.user.admire)
    if g.user.admire == None:
        admire = {}
    else:
        admire = json.loads(g.user.admire)
    if request.method == 'GET':
        passages = db.session.query(Resource.pid).all()
        for pid in passages:
            if str(pid[0]) in admire:
                continue
            else:
                admire[pid[0]] = False
        user = Users.query.filter_by(username = g.user.username).first()
        try:
            user.admire = json.dumps(admire)
        except TypeError:
            user.admire = admire
        admire = json.loads(user.admire)
        db.session.commit()
        db.session.close()
        return jsonify({"admire": admire,"tips": "Successed!", "code": 520})
    if request.method == 'POST':
        user = Users.query.filter_by(username = g.user.username).first()
        data = request.json
        user.admire = json.dumps(data)
        db.session.commit()
        db.session.close()
        return jsonify({"Tips": "Successed!", "code": 520})

@app.route('/api/v1/comments',methods=['GET','POST'])
def comments():
    if request.method == 'GET':
        pid = request.args.get('pid')
        comments = Comments.query.filter_by(pid=pid).all()
        rt_comments = {}
        for n in range(len(comments)):
            try:
                avatarPath = config.AVATARDIR + comments[n].username +'.jpg'
                avatar = sendImage(avatarPath)
            except FileNotFoundError:
                avatarPath = config.AVATARDIR + comments[n].username +'.png'
                avatar = sendImage(avatarPath)
            comments[n] = comments[n].to_json()
            comments[n]['avatar'] = avatar
            comments[n]['datetime'] = str(comments[n]['datetime'])[2:10]
        rt_comments = comments
        return jsonify(rt_comments)
    if request.method == 'POST':
        pid = request.json.get('pid')
        uid = request.json.get('uid')
        content = request.json.get('commit')
        username = request.json.get('username')
        timestamp = datetime.now()
        comment = Comments(pid,uid,content,username,timestamp)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'tips':'Successed!'})

@app.route('/api/v1/post/newpassage',methods=['POST'])
@auth.login_required
def new_passage():
    username = ((request.form).to_dict()).get('username')
    uid = ((request.form).to_dict()).get('uid')
    desc = ((request.form).to_dict()).get('imageDescription')
    pv = 0
    date = datetime.utcnow()
    img = request.files.get('imageFile')
    print(img.filename)
    imgName = username + '#' + img.filename
    path = basedir + "/static/img/"
    imagePath = './static/img/'+imgName
    filepath = path + imgName
    img.save(filepath)
    passage = Resource(uid,imagePath,desc,pv,username,date)
    print(imagePath)
    db.session.add(passage)
    db.session.commit()
    return jsonify({'tips':'Successed!'})

@app.route('/api/v1/admin',methods=['GET','POST'])
@auth.login_required
def content_manager():
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

def sendImage(path):
    with open(path, 'rb') as f:
        image = f.read()
        image = str(base64.b64encode(image))
    return image[2:-1]
if __name__ == '__main__':
    app.run()
