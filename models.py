from db import db
from werkzeug.security import generate_password_hash,check_password_hash

# SHOP

class ShopModel(db.Model):
    __tablename__='shops'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True,nullable=False)

    products=db.relationship('ProductModel',backref='shop',lazy='dynamic',cascade='all,delete')

    def __init__(self,name):
        self.name=name


# PRODUCT

class ProductModel(db.Model):
    __tablename__='products'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True,nullable=False)
    price=db.Column(db.Float(precision=2),nullable=False)
    shop_id=db.Column(db.Integer,db.ForeignKey('shops.id'),nullable=False,unique=False)

    def __init__(self,name,price,shop_id):
        self.name=name
        self.price=price
        self.shop_id=shop_id

# USER

class UserModel(db.Model):
    __tablename__='users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,nullable=False)
    password_hash=db.Column(db.String(64),nullable=False)

    def __init__(self,username,password):
        self.username=username
        self.password_hash=generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
                    

