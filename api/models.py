from sqla import db
from sqlalchemy.orm import validates

class UserModel(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(), nullable = False)
    password = db.Column(db.String(), nullable = False)
    shopping_lists = db.relationship('ShoppingList', backref='user_model', lazy=True)
    
    @validates('email', 'password')
    def validate_not_empty(self, key, value):
        if not value:
            raise ValueError(f'{key.capitalize()} is required.')
        return value
    
    def to_json(self):
        return {
            'id': self.id, 
            'email': self.email,
            'password': self.password
        }
 
class ShoppingList(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False, unique = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user_model.id'), nullable = False)
    creationDate = db.Column(db.DateTime(), nullable = False)
    productList = db.Column(db.String(), nullable = False)
    
    @validates('name', 'userId')
    def validate_not_empty(self, key, value):
        if not value:
            raise ValueError(f'{key.capitalize()} is required.')
        return value
    
    def to_json(self):
        return{
            'name':self.name,
            'userId':self.user_id,
            'creationDate':self.creationDate.strftime("%d/%m/%Y, %H:%M:%S"),
            'productList':self.productList
        }