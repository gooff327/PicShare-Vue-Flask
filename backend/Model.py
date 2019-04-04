from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from sqlalchemy import ForeignKey

from ext import db
from private_config import Config
from passlib.apps import custom_app_context
import json


class Users(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    avatar = db.Column(db.String(50))
    admire = db.Column(db.String(4096), default=None)
    brief = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    sex = db.Column(db.String(4))
    relation = db.relationship('Relation', order_by='Relation.id', backref='user')

    def __init__(self, username, email, avatar):
        self.username = username
        self.email = email
        self.avatar = avatar
        self.brief = None
        self.phone = None
        self.sex = '未设置'

    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'uid': self.uid})

    def verify_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = Users.query.get(data['uid'])
        return user

    def to_json(self):
        dict = self.__dict__
        print(type(dict))
        if "_sa_instance_state" in dict.keys():
            dict.pop('_sa_instance_state')
        return dict


class Resource(db.Model):
    __tablename__ = 'timeline'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, )
    img = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    pv = db.Column(db.Integer)
    author = db.Column(db.String(30))
    date = db.Column(db.DateTime)
    uavatar = db.Column(db.String(50))

    def __init__(self, uid, img, desc, pv, author, date):
        self.uid = uid
        self.img = img
        self.desc = desc
        self.pv = pv
        self.author = author
        self.date = date
        self.uavatar = author + '.jpg'

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Comments(db.Model):
    __tablename__ = 'comments'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(1024))
    username = db.Column(db.String(80))
    datetime = db.Column(db.DateTime)

    def __init__(self, pid, uid, comments, username, datetime):
        self.pid = pid
        self.uid = uid
        self.comments = comments
        self.username = username
        self.datetime = datetime

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Relation(db.Model):
    __tablename__ = 'relation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, ForeignKey('user.uid'))
    vid = db.Column(db.Integer)
    status = db.Column(db.Boolean)

    def __init__(self, uid, vid, status):
        self.uid = uid
        self.vid = vid
        self.status = status

    def to_json(self):
        dict = self.__dict__
        # if "_sa_instance_state" in dict:
        #     del dict["_sa_instance_state"]
        return dict


# m_type:
# 1 admire messages
# 2 comment messages
# 3 follow messages
# 4 forward messages
class Message(db.Model):
    __tablename__ = 'message'
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    vid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer)
    m_type = db.Column(db.Integer, nullable=False)
    m_content = db.Column(db.String(100))
    m_status = db.Column(db.Boolean, default=True)

    def __init__(self, uid, vid, pid, m_type, m_content, m_status):
        self.uid = uid
        self.vid = vid
        self.pid = pid
        self.m_type = m_type
        self.m_content = m_content
        self.m_status = m_status

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
