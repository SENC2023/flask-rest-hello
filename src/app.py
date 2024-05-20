"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Vehicles, FavoriteCharacters, FavoritePlanets, FavoriteVehicles

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user_query = User.query.filter_by(email=email).first()
    
    if user_query is None:
        return jsonify({"msg": "Email doesn't exist"}), 404

    if email != user_query.email or password != user_query.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(email=current_user).first()
    
    return jsonify({"result": user_query.serialize()}), 200

@app.route('/user', methods=['GET'])
def get_all_users():

    query_users = User.query.all()
    results_users = list(map(lambda item: item.serialize(), query_users))

    if query_users == []:
        return jsonify({"msg":"Users not found"}), 404
    else:
        return jsonify(results_users), 200

@app.route('/characters', methods=['GET'])
def get_all_characters():

    query_characters = Characters.query.all()
    results_characters = list(map(lambda item: item.serialize(), query_characters))

    if query_characters == []:
        return jsonify({"msg":"Characters not found"}), 404
    else:
        return jsonify(results_characters), 200


@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_id_character(characters_id):

    character_query = Characters.query.filter_by(id=characters_id).first()

    if character_query == None:
        return jsonify({"msg":"Character not found"}), 404
    else:
        return jsonify(character_query.serialize()), 200
    
@app.route('/planets', methods=['GET'])
def get_all_planets():

    query_planets = Planets.query.all()
    results_planets = list(map(lambda item: item.serialize(), query_planets))

    if query_planets == []:
        return jsonify({"msg":"Planets not found"}), 404
    else:
        return jsonify(results_planets), 200
    
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_id_planet(planets_id):

    planet_query = Planets.query.filter_by(id=planets_id).first()

    if planet_query == None:
        return jsonify({"msg":"Planet not found"}), 404
    else:
        return jsonify(planet_query.serialize()), 200

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    query_vehicles = Vehicles.query.all()
    results_vehicles = list(map(lambda item: item.serialize(), query_vehicles))

    if query_vehicles == []:
        return jsonify({"msg":"Vehicles not found"}), 404
    else:
        return jsonify(results_vehicles), 200
    
@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_id_vehicle(vehicles_id):

    vehicle_query = Vehicles.query.filter_by(id=vehicles_id).first()

    if vehicle_query == None:
        return jsonify({"msg":"Vehicle not found"}), 404
    else:
        return jsonify(vehicle_query.serialize()), 200
    
@app.route('/user/favorites/<int:user_id>', methods=['GET'])
@jwt_required()
def get_all_favorites_user(user_id):

    
    results_favorite_characters = FavoriteCharacters.query.filter_by(user=user_id).all()
    all_favorite_characters = [favorite.serialize() for favorite in results_favorite_characters]
    results_favorite_planets = FavoritePlanets.query.filter_by(user=user_id).all()
    all_favorite_planets = [favorite.serialize() for favorite in results_favorite_planets]
    results_favorite_vehicles = FavoriteVehicles.query.filter_by(user=user_id).all()
    all_favorite_vehicles = [favorite.serialize() for favorite in results_favorite_vehicles]

    return jsonify({
        "characters": all_favorite_characters,
        "planets": all_favorite_planets,
        "vehicles": all_favorite_vehicles
    })

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_favorite_planet(planet_id):

    user_id = request.json.get('user_id')

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    existing_favorite = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"message": "Planet is already a favorite"}), 400

    new_favorite = FavoritePlanets(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Planet added to favorites successfully"}), 201

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_new_favorite_character(character_id):

    user_id = request.json.get('user_id')

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404

    existing_favorite = FavoriteCharacters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_favorite:
        return jsonify({"message": "Character is already a favorite"}), 400

    new_favorite = FavoriteCharacters(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Character added to favorites successfully"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    
    favorite_planet = FavoritePlanets.query.filter_by(id=planet_id).first()

    if favorite_planet is None:
        return jsonify({"error": "Favorite planet not found"}), 404

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({"message": "Favorite planet deleted successfully"}), 200

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    
    favorite_character = FavoriteCharacters.query.filter_by(id=character_id).first()

    if favorite_character is None:
        return jsonify({"error": "Favorite character not found"}), 404

    db.session.delete(favorite_character)
    db.session.commit()

    return jsonify({"message": "Favorite character deleted successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
