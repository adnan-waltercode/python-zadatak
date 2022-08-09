from datetime import datetime, timedelta
from flask import request
from flask_restful import Api, Resource, fields, abort, reqparse
from passlib.hash import sha256_crypt
import jwt

from models import UserModel, ShoppingList
from models import db
from config import JWT_KEY
from middleware import decode_auth_token

api = Api()

class User(Resource):
    def post(self):
        reqData = request.get_json()
        userEmail = reqData['email']
        userPassword = reqData['password']
        hashedPassword = sha256_crypt.encrypt(userPassword)
        userModel = UserModel(email = userEmail, password = hashedPassword)
        db.session.add(userModel)
        db.session.commit()

        return userModel.to_json(), 201
    
    @decode_auth_token
    def put(self, *args, **kwargs):
        print(kwargs['user'])
        user = UserModel.query.filter_by(id = kwargs['user']).first()
        if not user:
            abort(400, message = "User not found")
        
        try:
            password = request.get_json()['password']
            hashedPassword = sha256_crypt.encrypt(password)
            user.password = hashedPassword
            db.session.commit()
            return 200
        except Exception as e:
            abort(500, message = "Server error")

class Login(Resource):
    def post(self):
        reqData = request.get_json()
        userEmail = reqData['email']
        userPassword = reqData['password']
        correctLogin = UserModel.query.filter_by(email = userEmail).first()

        if not correctLogin or not sha256_crypt.verify(userPassword, correctLogin.password):
            abort(400, message='Wrong username or password')
        
        try:
            jwtPayload = {
                'exp': datetime.utcnow() + timedelta(days = 0, hours = 5),
                'iat': datetime.utcnow(),
                'sub': userEmail
            }
            return jwt.encode(
                jwtPayload,
                JWT_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

shopping_parse_post = reqparse.RequestParser()
shopping_parse_post.add_argument('name', type = str, required = True)
shopping_parse_post.add_argument('userId', type = int, required = True)
shopping_parse_post.add_argument('productList', type = str, required = False)

class Shopping(Resource):
    @decode_auth_token
    def post(self):
        args = shopping_parse_post.parse_args()
            
        listName = args['name']
        userId = args['userId']
        productList = args['productList']
        
        if ShoppingList.query.filter_by(name = listName).first():
            abort(400, message = "Shopping list with this name already exists")
        
        
        newShoppingList = ShoppingList(
            name = listName,
            userId = userId,
            creationDate = datetime.utcnow(),
            productList = productList
        )
        try:
            db.session.add(newShoppingList)
            db.session.commit()
            
            return newShoppingList.to_json(), 201
        except Exception as e:
            abort(500, message="Server error")
    
    @decode_auth_token
    def delete(self):
        listId = request.args.get("listId")
        shoppingList = ShoppingList.query.filter_by(id = listId).first()
        if not shoppingList:
            abort(404, message = "List not found")
        try:
            db.session.delete(shoppingList)
            db.session.commit()
        except Exception as e:
            abort(500, message = "Server error")
        return '', 204
    
    @decode_auth_token
    def put(self):
        listId = request.args.get("listId")
        shoppingList = ShoppingList.query.filter_by(id = listId).first()
        if not shoppingList:
            abort(404, message = "List not found")
        data = request.get_json()
        newListName = data["name"]
        newListProducts = data["productList"]
        if newListName:
            shoppingList.name = newListName
        if newListProducts:
            shoppingList.productList = newListProducts
        try:
            db.session.commit()
        except Exception as e:
            abort(500, message = "Server error")
        return shoppingList.to_json(), 200
 
class Reporting(Resource):
    @decode_auth_token
    def get(self):
        from_date_arg = str(request.args.get("from"))
        to_date_arg = str(request.args.get("to"))
        if not from_date_arg or not to_date_arg:
            abort(400, message = "Parameters not provided")
        print(from_date_arg)
        print(to_date_arg)
        from_date = datetime.strptime(from_date_arg, '%d/%m/%Y')
        to_date = datetime.strptime(to_date_arg, '%d/%m/%Y')
        shopping_lists = ShoppingList.query.filter(ShoppingList.creationDate >= from_date).filter(ShoppingList.creationDate <= to_date)
        final_list = {}
        for list_entry in shopping_lists:
            products = list_entry.productList.split(',')
            for product in products:
                if product in final_list:
                    final_list[product] = final_list[product] + 1
                else:
                    final_list[product] = 1
        return final_list, 200  
        
api.add_resource(User, '/api/user')
api.add_resource(Login, '/api/login')
api.add_resource(Shopping, '/api/shopping')
api.add_resource(Reporting, '/api/reporting')