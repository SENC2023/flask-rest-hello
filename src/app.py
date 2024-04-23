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
from models import db, User, Characters, Planets, Vehicles
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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

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

# @app.route('/vehicles', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
