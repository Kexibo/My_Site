from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
metadata = db.metadata


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    favorite_games = db.relationship('FavoriteGame', backref='user', lazy=True)


# Таблица для отношения многие ко многим между пользователями и играми
class FavoriteGame(db.Model):
    __tablename__ = 'favorite_games'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_ru = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    users = db.relationship('FavoriteGame', backref='game', lazy=True)