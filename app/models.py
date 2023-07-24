from app import db
from app import login
from flask_login import UserMixin
from  werkzeug.security import check_password_hash
from  werkzeug.security import generate_password_hash
from sqlalchemy import DateTime


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    Path = db.relationship("Path")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Path(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    tag = db.Column(db.Integer)
    fname = db.Column(db.String(64))
    data = db.Column(DateTime)
    path = db.Column(db.String(128))
    mes = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #   需要先创建迁移脚本,不能直接运行 db.create_all()
    #   新字段允许为空,否则需要设置默认值或处理旧数据


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Fina(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(16))
    item = db.Column(db.String(32))
    vendor = db.Column(db.String(32))
    specificaction = db.Column(db.String(64))
    unit = db.Column(db.String(8))
    amount = db.Column(db.String(8))
    unit_price = db.Column(db.String(8))
    price = db.Column(db.String(8))
    remark= db.Column(db.String(16))
    category = db.Column(db.String(16))
    def __init__(self,dic):
        self.data=dic['data']
        self.item = dic['item']
        self.vendor = dic['vendor']
        self.specificaction = dic['specification']
        self.unit = dic['unit']
        self.amount = dic['amount']
        self.unit_price = dic['unit_price']
        self.price = dic['price']
        self.remark = dic['remark']
        self.category = dic['category']

class  Payment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    clientName = db.Column(db.String(8))
    productName = db.Column(db.String(8))
    price = db.Column(db.String(8))
    status = db.Column(db.Integer)
    time = db.Column(db.String)
    timeStart = db.Column(DateTime)
    timeEnd = db.Column(DateTime)
    note = db.Column(db.String(128))

