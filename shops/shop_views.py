from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import db
from models import ShopModel
from schemas import ShopSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

blueprint=Blueprint('shops',__name__,description='Operations on shops')

# CREATE AND GET SHOPS
@blueprint.route('/shop')
class ShopList(MethodView):
    @jwt_required()
    @blueprint.response(200,ShopSchema(many=True))
    def get(self):
        shops=ShopModel.query.all()
        return shops

    @jwt_required(fresh=True)
    @blueprint.arguments(ShopSchema)
    @blueprint.response(201,ShopSchema)
    def post(self,shop_data):
        shop=ShopModel(**shop_data)

        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError: 
            abort(400,message='A shop with that name already exist')
        except SQLAlchemyError:
            abort(500, message='An error occured  while inserting the shop') 
        
        return shop

# GET AND DELETE SHOP BY ID
@blueprint.route('/shop/<int:shop_id>')
class Shop(MethodView):
    
    @jwt_required()
    @blueprint.response(200,ShopSchema)
    def get(self,shop_id):
        shop=ShopModel.query.get_or_404(shop_id)
        return shop
    
    @jwt_required(fresh=True)
    def delete(self,shop_id):
        shop=ShopModel.query.get_or_404(shop_id)
        db.session.delete(shop)
        db.session.commit()
        return {'message':'Shop Deleted'}