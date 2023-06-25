#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = []
        all = Plant.query.all()
        for el in all:
            plants.append(el.to_dict())
        return make_response(jsonify(plants), 200)
    def post(self):
            new_plant = Plant(
            name=request.get_json()['name'],
            image=request.get_json()['image'],
            price=request.get_json()['price']
            )
            db.session.add(new_plant)
            db.session.commit()
            return make_response(jsonify(new_plant.to_dict()),202)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        return make_response(jsonify(plant.to_dict()), 200)
    def delete(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        db.session.delete(plant)
        db.session.commit()
        return make_response(jsonify(plant.to_dict()), 200)
    def patch(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        for attr in request.form:
            setattr(plant, attr, request.form.get(attr))
        db.session.commit()
        return make_response(jsonify(plant.to_dict()), 200)

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)