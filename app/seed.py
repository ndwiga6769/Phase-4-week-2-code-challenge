
from random import randint, choice

from faker import Faker

from app import app
from models import db, Pizza, Restaurant, PizzaRestaurant

fake = Faker()
  
with app.app_context():
    Pizza.query.delete()
    Restaurant.query.delete()
    PizzaRestaurant.query.delete()
    print("Seeding Restaurants \U0001F374")
    restaurant_names = [
    "Sottocasa NYC",
    "PizzArte",
    "SABOR LATINO RESTAURANT",
    "$1.25 PIZZA",
    "1001 NIGHTS CAFE",
    "1 2 3 BURGER SHOT BEER",
    "(LIBRARY)  FOUR & TWENTY BLACKBIRDS",
    "1 EAST 66TH STREET KITCHEN",
    "100 FUN"
    ]
    for name in restaurant_names:
        restaurant = Restaurant(name=name, address=fake.address())
        db.session.add(restaurant)
    
    print("Seeding Pizza \U0001F355")
    pizza_names = [
        "Cheese",
        "Pepperoni",
        "Margherita",
        "Hawaiian",
        "Meat Lovers",
        "Veggie",
        "BBQ Chicken",
        "Buffalo Chicken",
        "Supreme",
        "White Pizza"
    ]
    ingredients = ["mozzarella cheese", "pizza sauce", "olive oil","buffalo sauce","pepperoni","ham"]
    for name in pizza_names:
        pizza = Pizza(name=name, ingredients=",".join(ingredients))
        db.session.add(pizza)

    print("Seeding Pizza\U0001F355Restaurants\U0001F374")

    pizza_ids = [pizza.id for pizza in Pizza.query.all()]
    restaurant_ids = [restaurant.id for restaurant in Restaurant.query.all()]
    for _ in range(30):
        pizza_restaurant = PizzaRestaurant(price = randint(1,30),pizza_id = choice(pizza_ids),restaurant_id = choice(pizza_ids))
        db.session.add(pizza_restaurant)
    db.session.commit()
    print("Done Seeding \U0001F44D")

