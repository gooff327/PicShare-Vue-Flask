class config:
    DEBUG = True
    SECRET_KEY = 'goofftyy'
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = 'gooff'
    HOST = '144.202.125.147'
    PORT = '3306'
    DATABASE = 'vueflask'
    SQLALCHEMY_DATABASE_URI = DIALECT+'+pymysql://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AVATARDIR = './static/img/avatar/'
    IMAGEDIR = './static/img/'
