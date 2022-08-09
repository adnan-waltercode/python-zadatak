from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserModel(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(), nullable = False)
    password = db.Column(db.String(), nullable = False)
    
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password
        }

class ShoppingList(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False, unique = True)
    userId = db.Column(db.Integer(), nullable = False)
    creationDate = db.Column(db.DateTime(), nullable = False)
    productList = db.Column(db.String(), nullable = False)
    
    def to_json(self):
        return{
            'name':self.name,
            'userId':self.userId,
            'creationDate':self.creationDate.strftime("%d/%m/%Y, %H:%M:%S"),
            'productList':self.productList
        }