class config:
    DEBUG = True
    SECRET_KEY = 'goofftyy'
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = 'gooff'
    '''to VPS in US
    HOST = '204.44.85.176'
    DATABASE = 'vueflask'
    DATABASE = 'user_db'
'''
    HOST1 = '204.44.85.176'
    HOST = '127.0.0.1   '
    PORT = '3306'
    DATABASE = 'vueflask'
    SQLALCHEMY_DATABASE_URI = DIALECT+'+pymysql://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False