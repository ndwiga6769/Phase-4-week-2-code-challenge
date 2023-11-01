from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
    
class Restaurant(db.Model,SerializerMixin):
    __tablename__ = "restaurants"

    serialize_rules = ("-pizzas.restaurant")
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    address = db.Column(db.String(),nullable=False)
    pizzas = db.relationship('PizzaRestaurant', backref='restaurant')

class Pizza(db.Model,SerializerMixin):
    __tablename__ = "pizzas"
    serialize_rules = ("-restaurants.pizza")
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    ingredients = db.Column(db.String(500),nullable=False)
    restaurants = db.relationship('PizzaRestaurant', backref='pizza')

class PizzaRestaurant(db.Model,SerializerMixin):
    __tablename__ = "pizza_restaurants"
    serialize_rules = ("-restaurants.pizza,-pizzas.restaurant")
    id = db.Column(db.Integer(),primary_key=True)
    price= db.Column(db.Numeric(),nullable=False)
    pizza_id=db.Column(db.Integer(),db.ForeignKey("pizzas.id"),nullable=False)
    restaurant_id=db.Column(db.Integer(),db.ForeignKey("restaurants.id"),nullable=False)

    __table_args__ = (
        db.CheckConstraint('price >= 1 AND price <= 30', name='check_price'),
    )
    @validates('price')
    def validates_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price