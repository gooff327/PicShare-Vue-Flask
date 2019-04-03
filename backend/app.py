from filecmp import cmp
from qcloud_cos import CosS3Client

from flask import Flask, request, jsonify, g, json, make_response, render_template
from flask_cors import CORS
from sqlalchemy import func, and_
from ext import db
from private_config import Config
from private_config import BucketConfig
import base64
from Model import *
import os
from flask_httpauth import HTTPBasicAuth
from datetime import datetime


def upload_to_bucket(client, bucket, path, file_name):
    response = client.put_object_from_local_file(
        Bucket=bucket,
        LocalFilePath=path,
        Key=file_name,
    )
    print(response['ETag'])
    if os.path.exists(path):
        os.remove(path)


def get_file_url(client, bucket, file_name):
    response = client.get_presigned_download_url(
        Bucket=bucket,
        Key=file_name,
        Expired=3000
    )
    return response
    # pass


app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
app.config.from_object(Config)
CORS(app)
db.init_app(app)
auth = HTTPBasicAuth()
basedir = os.path.abspath(os.path.dirname(__file__))
bucket_client = BucketConfig()
img_client = CosS3Client(BucketConfig.img_bucket_config(bucket_client))
avatar_client = CosS3Client(BucketConfig.avatar_bucket_config(bucket_client))
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


@app.route('/', methods=['GET', 'POST'])
def index():
    print(basedir)
    return render_template('index.html')


@app.route('/api/v1/post/avatar', methods=['GET', 'POST'])
def get_avatar():
    if ((request.form).to_dict()).get('username'):
        username = ((request.form).to_dict()).get('username')
        img = request.files.get('file')
        save_avatar(img, username)
    else:
        filename = ((request.form).to_dict()).get('filename')
        img = request.files.get('avatar')
        save_avatar(img, filename)
    return None


@app.route('/api/v1/register', methods=['GET', 'POST'])
def register():
    '''can remove the '#' to create the user table ! '''
    db.create_all()
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    if Users.query.filter_by(username=username).first():
        return jsonify({'username': username, 'password': password, 'tips': 'Reppeat of username!', 'err_code': 402})
    elif Users.query.filter_by(email=email).first():
        return jsonify({'username': username, 'password': password, 'tips': "This email has signed!", 'err_code': 403})
    avatar = username + '.jpg'
    user = Users(username, email, avatar)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': username, 'password': password, 'tips': 'Okay,you can sign in now!', 'err_code': 200})


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
def verify_password(username_or_token, password):
    if request.path == '/api/v1/login':
        user = Users.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    else:
        user = Users.verify_token(username_or_token)
        if not user:
            return False
    g.user = user
    return True


@app.route('/api/v1/login', methods=['GET', 'POST'])
@auth.login_required
def get_token():
    user = {}
    token = g.user.generate_auth_token()
    user['following'] = resolve_following_relation(g.user.relation)
    user['username'] = g.user.username
    user['uid'] = g.user.uid
    user['brief'] = g.user.brief
    user['email'] = g.user.email
    user['avatar'] = get_file_url(avatar_client, Config.avatar_bucket, g.user.avatar)
    user['phone'] = g.user.phone
    user['sex'] = g.user.sex
    return jsonify({'token': token.decode('ascii'), 'user': user})


'''
Api to get resource
Content-Type:application/json
input:
{
    "username":"xxx",
    ...
}
'''


@app.route('/api/v1/resources', methods=['GET', 'POST'])
@auth.login_required
def resource():
    db.create_all()
    datas = {}
    current_path = request.args.get('currentPath')
    start_index = int(request.args.get('startIndex'))
    last_index = int(request.args.get('lastIndex'))
    if current_path == 'home':
        datas = query_passages(start_index, last_index, types=1, keyword=None)
    elif current_path == 'following':
        datas = query_passages(start_index, last_index, types=2, keyword=g.user.uid)
    return jsonify(datas[0])


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


@app.route('/api/v1/admire', methods=['GET', 'POST'])
@auth.login_required
def admire():
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
        user = Users.query.filter_by(username=g.user.username).first()
        try:
            user.admire = json.dumps(admire)
        except TypeError:
            user.admire = admire
        admire = json.loads(user.admire)
        db.session.commit()
        db.session.close()
        return jsonify({"admire": admire, "tips": "Successed!", "code": 521})
    if request.method == 'POST':
        user = Users.query.filter_by(username=g.user.username).first()
        content = '觉得很赞'
        data = request.json
        admire_list = json.loads(data['admireList'])
        admire_this = json.loads(data['admireThis'])
        message = Message(m_content=content, uid=g.user.uid, vid=admire_this['uid'], pid=admire_this['pid'], m_type=1,
                          m_status=1)
        if admire_this['result']:
            add_admire_message(admire_this['pid'])
        else:
            remove_admire_message(admire_this['pid'])
        user.admire = json.dumps(admire_list)
        db.session.commit()
        db.session.close()
        return jsonify({"Tips": "Successed!", "code": 520})


@app.route('/api/v1/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'GET':
        pid = request.args.get('pid')
        query_comments = Comments.query.filter_by(pid=pid).order_by(Comments.datetime.desc()).all()  # 此处应该注意查询时排序
        rt_comments = {}
        for n in range(len(query_comments)):
            avatarPath = query_comments[n].username + '.jpg'
            avatar = get_file_url(avatar_client, Config.avatar_bucket, avatarPath)
            query_comments[n] = query_comments[n].to_json()
            query_comments[n]['avatar'] = avatar
            query_comments[n]['datetime'] = str(query_comments[n]['datetime'])[2:10]
        rt_comments = query_comments
        return jsonify(rt_comments)
    if request.method == 'POST':
        pid = request.json.get('pid')
        uid = request.json.get('uid')
        vid = request.json.get('vid')
        content = request.json.get('commit')
        username = request.json.get('username')
        timestamp = datetime.now()
        comment = Comments(pid, uid, content, username, timestamp)
        message = Message(m_type=2, uid=uid, vid=vid, m_content=content, m_status=1, pid=pid)
        db.session.add(comment)
        db.session.add(message)
        db.session.commit()
        return jsonify({'tips': 'Successed!'})


@app.route('/api/v1/post/newpassage', methods=['POST'])
@auth.login_required
def new_passage():
    username = g.user.username
    uid = g.user.uid
    desc = ((request.form).to_dict()).get('imageDescription')
    pv = 0
    date = datetime.utcnow()
    img = request.files.get('imageFile')
    imgName = username + '#' + img.filename
    path = basedir + "/static/img/"
    imagePath = Config.IMAGEDIR + imgName
    filepath = path + imgName
    img.save(filepath)
    upload_to_bucket(img_client, Config.img_bucket, imagePath, imgName)
    passage = Resource(uid, imgName, desc, pv, username, date)
    db.session.add(passage)
    db.session.commit()
    return jsonify({'tips': 'Successed!'})


@app.route('/api/v1/get/users', methods=['GET'])
@auth.login_required
def get_users():
    type = request.args.get('type')
    keyword = int(request.args.get('uid'))
    if type == 'followings':
        vid_sub = Relation.query.filter_by(uid=keyword).with_entities(Relation.vid.label('vid')).subquery()
        users = db.session.query(Users, vid_sub.c.vid).join(vid_sub, Users.uid == vid_sub.c.vid).with_entities(
            Users).all()
        users = resolve_users(users)
        return jsonify({'tips': 'Successed!', 'userList': users})

    elif type == 'followers':
        uid_sub = Relation.query.filter_by(vid=keyword).with_entities(Relation.uid.label('uid')).subquery()
        users = db.session.query(Users, uid_sub.c.uid).join(uid_sub, Users.uid == uid_sub.c.uid).with_entities(
            Users).all()
        users = resolve_users(users)
    return jsonify({'tips': 'Successed!', 'userList': users})


def resolve_users(users):
    rt_users = []
    for user in users:
        lite_user = {}
        lite_user['uid'] = user.uid
        lite_user['username'] = user.username
        lite_user['brief'] = user.brief
        print(type(user))
        lite_user['avatar'] = get_file_url(avatar_client, Config.avatar_bucket, user.avatar)
        rt_users.append(lite_user)
    return rt_users


@app.route('/api/v1/query/user', methods=['GET'])
@auth.login_required
def query_user():
    with db.session.no_autoflush:
        db.create_all()
        rt_user = {}
        start_index = int(request.args.get('startIndex'))
        last_index = int(request.args.get('lastIndex'))
        key = request.args.get('username')
        user = Users.query.filter_by(username=key).first()
        produces = Resource.query.filter_by(author=key).all()
        followers = Relation.query.filter_by(vid=user.uid).all()
        res = query_passages(start_index, last_index, types=3, keyword=key)
        # avatar_path = config.AVATARDIR + user.avatar

        rt_user['produces'] = len(produces)
        rt_user['followers'] = len(followers)
        rt_user['following'] = len(user.relation)
        rt_user['username'] = user.username
        rt_user['uid'] = user.uid
        rt_user['brief'] = user.brief
        rt_user['avatar'] = get_file_url(avatar_client, Config.avatar_bucket, user.avatar)
        rt_user['sex'] = user.sex
        if res[0] == {}:
            return jsonify({'tips': 'All loaded!', 'user': rt_user, 'contents': res[0]})
    return jsonify({'tips': 'Successed!', 'user': rt_user, 'contents': res[0]})


@app.route('/api/v1/concern/action', methods=['POST'])
@auth.login_required
def concern_action():
    vid = ((request.form).to_dict()).get('vid')
    status = get_bool_status((request.form).to_dict().get('status'))
    concern_content = '关注了你'
    cancel_concern_content = '对你取消了关注'
    uid = g.user.uid
    relation = Relation.query.filter_by(uid=uid, vid=vid).first()
    if (status == True):
        message = Message(m_content=concern_content, uid=uid, vid=vid, m_status=1, m_type=3, pid=-1)
        relation = Relation(uid=uid, vid=vid, status=status)
        db.session.add(relation)
        db.session.add(message)
        db.session.commit()
    elif (status == False):
        message = Message(m_content=cancel_concern_content, uid=uid, vid=vid, m_status=1, m_type=3, pid=-1)
        db.session.delete(relation)
        db.session.add(message)
        db.session.commit()
    return jsonify({'tips': 'Successed!'})


@app.route('/api/v1/edit/profile', methods=['POST'])
@auth.login_required
def edit_profile():
    rt_user = {}
    avatar = request.files.get('avatar')
    brief = ((request.form).to_dict()).get('brief')
    sex = ((request.form).to_dict()).get('sex')
    phone = ((request.form).to_dict()).get('phone')
    user = Users.query.filter_by(uid=g.user.uid).first()
    if avatar is not None:
        save_avatar(avatar, g.user.username)
    else:
        pass
    user.brief = brief
    user.sex = sex
    user.phone = phone
    db.session.commit()
    rt_user['username'] = g.user.username
    rt_user['uid'] = g.user.uid
    rt_user['brief'] = g.user.brief
    rt_user['email'] = g.user.email
    rt_user['avatar'] = get_file_url(avatar_client, Config.avatar_bucket, g.user.avatar)
    rt_user['phone'] = g.user.phone
    rt_user['sex'] = g.user.sex
    return jsonify({'tips': 'Successed!', 'user': rt_user})


@app.route('/api/v1/get/messages')
@auth.login_required
def get_messages():
    m_type = None
    message_type = request.args.get('messageType')
    type_dict = {
        'admire': 1,
        'comment': 2,
        'follow': 3,
        'forward': 4,
    }
    if message_type in type_dict.keys():
        m_type = type_dict.get(message_type)
    rt_messages = {}
    if m_type is not None:
        messages = Message.query.filter(
            and_(Message.vid == g.user.uid, Message.m_type == m_type, Message.uid != g.user.uid)).all()
        rt_messages = resolve_message_detail(messages)
        return jsonify({'messageDetails': rt_messages})
    else:
        admire_messages = Message.query.filter_by(vid=g.user.uid, m_type=1).all()
        admire_messages = resolve_messages(admire_messages)
        comment_messages = Message.query.filter_by(vid=g.user.uid, m_type=2).all()
        comment_messages = resolve_messages(comment_messages)
        follow_messages = Message.query.filter_by(vid=g.user.uid, m_type=3).all()
        follow_messages = resolve_messages(follow_messages)
        forward_messages = Message.query.filter_by(vid=g.user.uid, m_type=4).all()
        forward_messages = resolve_messages(forward_messages)
        rt_messages['admire_messages'] = admire_messages
        rt_messages['comment_messages'] = comment_messages
        rt_messages['follow_messages'] = follow_messages
        rt_messages['forward_messages'] = forward_messages
        return jsonify({'messages': rt_messages})


@app.route('/api/v1/messages/query', methods=['POST'])
@auth.login_required
def query_items():
    query_list = request.json
    result = {}
    result['users'] = query_by_list(Users, query_list['users'])
    result['passages'] = query_by_list(Resource, query_list['passages'])
    return jsonify(result)


def query_by_list(cls, query_list):
    result = {}
    if cls == Users:
        for el in query_list:
            content = cls.query.filter_by(uid=el).first().to_json()
            content['avatar'] = get_file_url(avatar_client, Config.avatar_bucket, content['avatar'])
            result[content['uid']] = content
    elif cls == Resource:
        for el in query_list:
            if el <= 0:
                pass
            elif el > 0:
                content = cls.query.filter_by(pid=el).first().to_json()
                content['img'] = get_file_url(img_client, Config.img_bucket, content['img'])
                result[content['pid']] = content
    return result


@app.route('/api/v1/put/message/status', methods=['PUT'])
@auth.login_required
def change_message_status():
    read_messages = request.json
    print(read_messages)
    for el in read_messages:
        print(el)
        message = Message.query.filter_by(mid=el).first()
        message.m_status = 0
        db.session.commit()
    return jsonify('ok')


app.route('/api/v1/logout')


@auth.login_required
def logout():
    username = request.args.get('username')
    print(username)
    return jsonify({'data': username + ' log out'})


def get_bool_status(str):
    return True if str.lower() == 'true' else False


def resolve_following_relation(relations):
    rt_relations = {}
    for relation in relations:
        relation = relation.to_json()
        rt_relations[relation['vid']] = relation['status']
    print(rt_relations)
    return rt_relations


def resolve_followers_relation(relations):
    rt_relations = {}
    for relation in relations:
        relation = relation.to_json()
        rt_relations[relation['uid']] = relation['status']
    print(rt_relations)
    return rt_relations


def resolve_messages(messages):
    rt_messages = {}
    for i in range(0, len(messages)):
        # 过滤掉自己给自己的赞
        if not messages[i].vid == messages[i].uid:
            messages[i] = messages[i].to_json()
            rt_messages[i] = messages[i]
    return rt_messages


def resolve_message_detail(messages):
    users = {}
    passages = {}
    rt_messages = {}
    for i in range(0, len(messages)):
        user_key = messages[i].uid
        passage_key = messages[i].pid
        if messages[i].uid not in users.keys and messages[i].pid not in passages.keys():
            temp_user = Users.query.filter_by(uid=messages[i].uid).first().to_json()
            temp_passage = Resource.query.filter_by(pid=messages[i].pid).first().to_json()
            users[user_key] = {'username': temp_user['username'],
                               'avatar': get_file_url(avatar_client, Config.img_bucket, temp_user['avatar'])
                               }
            passage = {'img': get_file_url(img_client, Config.img_bucket, temp_passage['img']),
                       'desc': temp_passage['desc']}
            passages[passage_key] = passage
        rt_messages = messages
        rt_messages[i] = messages[i].to_json()
        print(len(passages))
    return rt_messages, users, passages


def query_passages(start_index, last_index, types, keyword):
    data = {}
    res = []
    if types == 1:
        passages = Resource.query.order_by(Resource.date.desc()).all()
        # 好友动态
    elif types == 2:
        # 保存获取好友id的sql语句
        vid_stub = Relation.query.filter_by(uid=keyword).with_entities(Relation.vid.label('vid')).subquery()
        # 通过uid进行join查询好友动态
        passages = db.session.query(Resource, vid_stub.c.vid).join(vid_stub,
                                                                   Resource.uid == vid_stub.c.vid).with_entities(
            Resource).order_by(Resource.date.desc()).all()
    elif types == 3:
        passages = Resource.query.filter_by(author=keyword).order_by(Resource.date.desc()).all()
    else:
        return None
    amount = len(passages)
    if last_index > amount:
        passages = passages[start_index:]
    elif start_index > amount:
        res.append(data)
        res.append(amount)
        return res
    else:
        passages = passages[start_index:last_index]
    for passage in passages:
        passage.uavatar = get_file_url(avatar_client, Config.avatar_bucket, passage.uavatar)
        passage.img = get_file_url(img_client, Config.img_bucket, passage.img)
    for n in range(len(passages)):
        data[start_index + n] = passages[n].to_json()
    res.append(data)
    res.append(amount)
    return res


def save_avatar(img, username):
    imageName = username + '.jpg'
    path = basedir + "/static/img/avatar/"
    filepath = path + imageName
    img.save(filepath)
    upload_to_bucket(avatar_client, Config.avatar_bucket, filepath, imageName)


# when user like others passages,make a message into server for sending t authors
def add_admire_message(pid):
    db.create_all()
    uid = g.user.uid
    vid = Resource.query.filter_by(pid=pid).first().uid  # get author uid
    m_type = 1
    pid = pid
    m_content = '觉得很赞'
    m_status = True
    if not (Message.query.filter_by(uid=g.user.uid, pid=pid).first()):
        admire_message = Message(uid=uid, vid=vid, pid=pid, m_type=m_type, m_content=m_content, m_status=m_status)
    db.session.add(admire_message)
    db.session.commit()


def remove_admire_message(pid):
    admire_message = Message.query.filter_by(pid=pid, uid=g.user.uid).first()
    if admire_message:
        db.session.delete(admire_message)
        db.session.commit()


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
