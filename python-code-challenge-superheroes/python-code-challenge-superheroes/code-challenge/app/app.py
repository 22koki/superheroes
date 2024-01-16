#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

import os
abs_path=os.getcwd()

db_path=f'{abs_path}/db/app.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False  # Keep the order of keys in JSON responses

migrate = Migrate(app, db)
db.init_app(app)

# Routes

@app.route('/')
def home():
    return ''

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

# GET /heroes/:id
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    try:
        hero = Hero.query.get_or_404(hero_id)
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_data)

# GET /powers/:id
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    try:
        power = Power.query.get_or_404(power_id)
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PATCH /powers/:id
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    try:
        power = Power.query.get_or_404(power_id)
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        else:
            return jsonify({'error': 'No valid fields provided for update'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    try:
        hero_power = HeroPower(strength=data['strength'], power_id=data['power_id'], hero_id=data['hero_id'])
        db.session.add(hero_power)
        db.session.commit()
        hero = Hero.query.get_or_404(data['hero_id'])
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555)
