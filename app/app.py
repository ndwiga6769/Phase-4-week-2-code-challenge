from flask import request, session,jsonify,make_response
from flask_restful import Resource
from config import db,app,api
from models import db, Pizza, Restaurant, PizzaRestaurant
class Home(Resource):
    def get(self):
        response = make_response(jsonify({
            "message":"Pizza Restaurant API",
        }))    
        return response    
api.add_resource(Home,"/")
class RestaurantResource(Resource):
    def get(self):  
        restaurants = Restaurant.query.all()
        
        restaurant_dict = [{
            "id":restaurant.id,
            "name":restaurant.name,
            "address":restaurant.address
        }for restaurant in restaurants]

        response = make_response(jsonify(restaurant_dict),200)
        return response
class RestaurantResourceById(Resource):
    def get(self,id):
        restaurant= Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict = {
                "id":restaurant.id,
                "name":restaurant.name,
                "address":restaurant.address,
                "pizzas": [{
                    "id":pizza_restaurant.pizza.id,
                    "name":pizza_restaurant.pizza.name,
                    "ingredients":pizza_restaurant.pizza.ingredients
                } for pizza_restaurant in restaurant.pizzas]
            }
            response = make_response(jsonify(restaurant_dict),200)
            return response
        else:
            return {"error": "Restaurant not found"}, 404
    def delete(self,id):
        restaurant= Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_pizzas = PizzaRestaurant.query.filter_by(restaurant_id = id).all()
            for rest in restaurant_pizzas:
                db.session.delete(rest)
            db.session.delete(restaurant)
            db.session.commit()
            return make_response(jsonify({"message": "Restaurant deleted Successfully"},204))
        else:
            return {"error": "Restaurant not found"}, 404
class PizzasResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()

        pizza_dict = [{
            "id":pizza.id,
            "name":pizza.name,
            "ingredients":pizza.ingredients
        }for pizza in pizzas]
        response = make_response(jsonify(pizza_dict),200)
        return response
class PizzaRestaurantResource(Resource):
    def get(self):
        pizza_restaurants = PizzaRestaurant.query.all()
        pizza_restaurant_dict = [{
            "price":round(pizza_restaurant.price,2),
            "restaurant_id":pizza_restaurant.restaurant_id,
            "pizza_id":pizza_restaurant.pizza_id
        }for pizza_restaurant in pizza_restaurants]

        response = make_response(jsonify(pizza_restaurant_dict),200)
        return response
    def post(self):
        data = request.get_json()
        price = data["price"]
        pizza_id = data["pizza_id"]
        restaurant_id = data["restaurant_id"]

        if not price and not pizza_id and not restaurant_id:
            return make_response(jsonify({"error":"Missing arguments"}), 400)
        else:
            pizza = Pizza.query.filter(Pizza.id == pizza_id).first()
            restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).first()
            if not pizza and not restaurant:
                return make_response(jsonify({'errors': ['Invalid pizza or restaurant ID']}), 400)
            else:
                pizza_restaurant = PizzaRestaurant(price=price,restaurant=restaurant,pizza=pizza)
                db.session.add(pizza_restaurant)
                db.session.commit()
            pizza_data = {
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            }
            return make_response(jsonify(pizza_data), 201 ) 
api.add_resource(PizzaRestaurantResource,"/restaurant_pizzas")
api.add_resource(PizzasResource,"/pizzas")
api.add_resource(RestaurantResourceById,'/restaurants/<int:id>')
api.add_resource(RestaurantResource,'/restaurants')
if __name__ == '__main__':
    app.run(port=5555, debug=True)