from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import DateTime

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256),nullable = False)
    super_name = db.Column(db.String)
    created_at = db.Column(DateTime, default = datetime.utcnow)
    updated_at = db.Column(DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

    powers = db.relationship('Power', secondary='heroPowers', back_populates='heroes')

    def __init__(self, name, super_name):
        self.name = name  # Assign 'name' argument to the 'name' attribute
        self.super_name = super_name  # Assign 'super_name' argument to the 'super_name' attribute

    def __repr__(self):
        return f'<Hero(name={self.name}, super_name={self.super_name})>'


class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256),nullable = False)
    description = db.Column(db.String)
    created_at = db.Column(DateTime, default = datetime.utcnow)
    updated_at = db.Column(DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

    heroes = db.relationship('Hero', secondary='heroPowers', back_populates='powers')

    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError("Description must be present.")
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

    def __init__(self, name, description):  # Update the constructor
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Power(name={self.name}, description={self.description})>'

class HeroPower(db.Model):
    __tablename__ = 'heroPowers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # hero = db.relationship('Power', back_populates='powers')
    # power = db.relationship('Hero', back_populates='heroes')                              
    # hero = db.relationship('Power', backref=db.backref('heroes', cascade='all, delete'))
    # powers = db.relationship('Power', backref=db.backref('powers', cascade='all, delete'))

    def __init__(self, strength, hero, power):  # Update the constructor
        self.strength = strength
        self.power_id = power.id
        self.hero_id = hero.id

    def __repr__(self):
        return f'<Hero(name={self.name}, super_name={self.super_name})>'

    @validates('strength')
    def validate_strength(self, key, value):
        strengths = ['Strong', 'Weak', 'Average']
        if not value:
            return ValueError('cannot be empty')
        if len(value) > 50:
            return ValueError('Strength exceeded 50 characters length')
        if value not in strengths:
            raise ValueError("Strength should be one of ['Strong', 'Weak', 'Average']")
        return value