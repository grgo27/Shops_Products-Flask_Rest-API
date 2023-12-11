from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import db
from models import UserModel
from schemas import UserSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token,get_jwt,jwt_required,create_refresh_token, get_jwt_identity
from blacklist import BLACKLIST

blueprint=Blueprint('users',__name__,description='Operations on users')

# REGISTER USER

@blueprint.route('/register')
class UserRegister(MethodView):

    @blueprint.arguments(UserSchema)
    def post(self,user_data):
        
        if UserModel.query.filter_by(username=user_data['username']).first():
            abort(409,message='Provided username already exist')

        user=UserModel(**user_data)
        db.session.add(user)
        db.session.commit()

        return {'message':'User created successfully'},201

# GET USERS
@blueprint.route('/user')
class User(MethodView):
    
    @blueprint.response(200,UserSchema(many=True))
    def get(self):
        users=UserModel.query.all()
        return users

# LOGIN USER
@blueprint.route('/login')
class UserRegister(MethodView):
    
    @blueprint.arguments(UserSchema)
    def post(self,user_data):
        
        user=UserModel.query.filter_by(username=user_data['username']).first()

        if user is not None and user.check_password(user_data['password']):

            access_token=create_access_token(identity=user.id,fresh=True)
            refresh_token=create_refresh_token(user.id)

            return {'access_token':access_token,'refresh_token':refresh_token},200
        
        abort(401,message='Invalid credentials')
    
# LOGOUT
@blueprint.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def delete(self): 
        jti=get_jwt()['jti'] 
        BLACKLIST.add(jti) 
        return {'message':'Succesfully logged out'},200

# REFRESH TOKEN
@blueprint.route('/refresh')
class TokenRefresh(MethodView): 
    
    @jwt_required(fresh=True)
    def post(self):
        current_user=get_jwt_identity()
        new_token=create_access_token(identity=current_user,fresh=False) 
        
        jti=get_jwt()['jti'] 
        BLACKLIST.add(jti)

        return {'access_token':new_token},200