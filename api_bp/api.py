from flask import Blueprint, jsonify, current_app, request, abort
from models import User, Game
import jwt
from datetime import datetime, timedelta, timezone
from .decorator import token_required

api_bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")


@api_bp.route('/')
def api_index():
    return jsonify({"status": 200})


@api_bp.route('/get_games')
@token_required
def get_games():
    games = Game.query.all()
    result = {}
    for game in games:
        result[game.id] = {"name_en": game.name_en,
                           "name_ru": game.name_ru,
                           "tags": game.tags,
                           "url": game.url}
    return jsonify({"games": result})


@api_bp.route('/get_game_by_name', methods=["GET", "POST"])
@token_required
def get_game_by_name():
    if request.method == "POST":
        game_name = request.json.get("name_en")
        game = Game.query.filter(Game.name_en == game_name).first()
        result = {
            game.name_en: {
                "id": game.id,
                "name_ru": game.name_ru,
                "tags": game.tags,
                "url": game.url
            }
        }
        return jsonify(result)
    return abort(405)


@api_bp.route('/get_game_by_id', methods=["GET", "POST"])
@token_required
def get_game_by_id():
    if request.method == "POST":
        game_id = request.json.get("id")
        game = Game.query.filter(Game.id == game_id).first()
        result = {
            game.id: {
                "name_en": game.name_en,
                "name_ru": game.name_ru,
                "tags": game.tags,
                "url": game.url
            }
        }
        return jsonify(result)
    return abort(405)


@api_bp.route('/get_user', methods=["GET", "POST"])
@token_required
def get_user():
    if request.method == "POST":
        user_id = request.json.get("id")
        user = User.query.filter(User.id == user_id).first()
        result = {
            user.id: {
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }
        return jsonify(result)
    return abort(405)


@api_bp.route('/get_user_by_name', methods=["GET", "POST"])
@token_required
def get_user_by_id():
    if request.method == "POST":
        username = request.json.get("username")
        user = User.query.filter(User.username == username).first()
        result = {
            user.username: {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }
        return jsonify(result)
    return abort(405)


@api_bp.route('/auth', methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")
        exp = datetime.now(tz=timezone.utc) + timedelta(hours=1)
        token = jwt.encode(dict(email=email, password=password, exp=exp), current_app.secret_key,
                           algorithm="HS256")
        return {"status": "token generated successfully", "token": token}
    return abort(405)
