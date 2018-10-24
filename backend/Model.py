from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from ext import db
from config import config
from passlib.apps import custom_app_context
import json
class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

    def __init__(self,username,email):
        self.username = username
        self.email = email

    def hash_password(self,password):
        self.password = custom_app_context.encrypt(password)


    def verify_password(self,password):
        return custom_app_context.verify(password,self.password)


    def generate_auth_token(self,expiration = 6000):
        s = Serializer(config.SECRET_KEY,expires_in=expiration)
        return s.dumps({'id': self.id})

    def verify_token(token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = Users.query.get(data['id'])
        return user

class Resource(db.Model):
    __tablename__ =  'resourse'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(80))
    cls = db.Column(db.String(20))
    img = db.Column(db.String(200))
    content = db.Column(db.String(300))
    pv = db.Column(db.Integer)
    author = db.Column(db.String(30))
    date = db.Column(db.DateTime)

    def __init__(self,title,cls,img,content,pv,author,date):
        self.title = title
        self.cls = cls
        self.img = img
        self.content = content
        self.pv = pv
        self.author = author
        self.date = date

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

