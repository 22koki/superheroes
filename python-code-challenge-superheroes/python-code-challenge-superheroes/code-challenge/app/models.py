# app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    # Relationship with HeroPower model
    hero_powers = db.relationship('HeroPower', back_populates='hero')

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # Relationship with HeroPower model
    hero_powers = db.relationship('HeroPower', back_populates='power')

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), primary_key=True)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), primary_key=True)
    strength = db.Column(db.String(50), nullable=False)

    # Relationships with Hero and Power models
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

# This line is added to configure the relationships properly
db.configure_mappers()
