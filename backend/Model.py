from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ext import db
from config import config
class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Users {}>'.format(self.username)