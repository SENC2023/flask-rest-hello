from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_characters = db.relationship('FavoriteCharacters', backref = 'users', lazy = True)
    favorite_planets = db.relationship('FavoritePlanets', backref = 'users', lazy = True)
    favorite_vehicles = db.relationship('FavoriteVehicles', backref = 'users', lazy = True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    favorite_characters = db.relationship('FavoriteCharacters', backref = 'character', lazy = True)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250),nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    favorite_planets = db.relationship('FavoritePlanets', backref = 'planet', lazy = True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250),nullable=False)
    vehicle_class = db.Column(db.String(250),nullable=False)
    length = db.Column(db.String(250),nullable=False)
    favorite_vehicles = db.relationship('FavoriteVehicles', backref = 'vehicle', lazy = True)

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "length": self.length,
        }
    
# class FavoriteUser(db.Model):
#     __tablename__ = 'favorite_user'
#     id = db.Column(db.Integer, primary_key=True)
#     user = db.Column(db.Integer, db.ForeignKey('user.id'))
#     characters = db.Column(db.Integer, db.ForeignKey('characters.id'))
#     planets = db.Column(db.Integer, db.ForeignKey('planets.id'))

#     def __repr__(self):
#         return '<FavoriteUser %r>' % self.id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user": self.user,
#             "characters": self.characters,
#             "planets": self.planets,
#         }
    
class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    def __repr__(self):
        return '<FavoriteCharacters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "characters": self.characters
        }
    
class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def __repr__(self):
        return '<FavoritePlanets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user,
            "planet_id": self.planets,
        }
    
class FavoriteVehicles(db.Model):
    __tablename__ = 'favorite_vehicles'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicles = db.Column(db.Integer, db.ForeignKey('vehicles.id'))

    def __repr__(self):
        return '<FavoriteVehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "vehicles": self.vehicles,
        }