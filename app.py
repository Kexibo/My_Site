# Его величество Фласк
from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session, \
    make_response, Response
# База данных
from models import User, db, Game, FavoriteGame
# Авторизация
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
# Хеширование пароля
from werkzeug.security import generate_password_hash, check_password_hash
# Взаимодействие с компьютером
import os
from sqlalchemy import or_
# Почта
from flask_mail import Mail, Message
# Время
from datetime import datetime
# Админ панель
from flask_admin import Admin
from adminview import MyAdminIndexView, MyModelView, GameView
# API
from api_bp.api import api_bp
# Старое хэширование
import hashlib

# --------------------------------------------------- Начало начал -----------------------------------------------------
app = Flask(__name__)  # инициализируем экземпляр нашего приложения
app.config['SECRET_KEY'] = 'sdfhsdjkghsdhgjksd'  # os.getenv('SECRET_KEY')  # наш ключ

# ----------------- Прописываем конфигурацию нашего приложения(лучше это вынести в отдельный файл config) --------------
# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Конфигурация почтового сервиса
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# ---------------------- создаем сущности для работы модулей(лучше вынести в отдельный файл __init__.py) ---------------
db.init_app(app)  # инициализируем приложение в бд

mail = Mail(app)  # создаем сущность для работы с почтой

login_manager = LoginManager()  # сущность для работы flask-login
login_manager.init_app(app)  # инициализируем приложение для flask-login

admin = Admin(app, index_view=MyAdminIndexView(), name='ExampleStore',
              template_mode='bootstrap3')  # сущность для работы админки
admin.add_view(MyModelView(User, db.session))
admin.add_view(GameView(Game, db.session))

app.register_blueprint(api_bp, url_prefix="/api")


# ----------------------------------------------------------------------------------------------------------------------


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


# ----------------------------- Далее идут функции-представления для маршрутов приложения ------------------------------


# Основные страницы
@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/choose')
@login_required
def choose():
    try:
        games = Game.query.all()
        fav_ids = [fav.game_id for fav in FavoriteGame.query.filter_by(user_id=current_user.id).all()]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("choose.html", games=[], fav=[])

    return render_template("choose.html", games=games, fav=fav_ids)


@app.route('/goods')
def goods():
    return render_template("goods.html")


@app.route('/news')
def news():
    return render_template("news.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        msg = Message("Вам поступило новое обращение на сайте", recipients=[name])
        msg.body = f"Клиент оставил номер телефона:{phone} и сообщение: {message}"
        mail.send(msg)
        return redirect('/thanks')
    else:
        return render_template("contact.html")


@app.route('/about')
def about():
    return render_template("about.html")


# Регистрация пользователя
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')
        try:
            try:
                user = User.query.filter(User.email == email).one()
            except:
                flash("Неверный логин или пароль")
                return redirect("/signin")
            if user and hashlib.sha224(password.encode()).hexdigest() == user.password:
                if user.role == 2:
                    login_user(user)
                    print('2')
                    return render_template('index.html')
                else:
                    login_user(user)
                    return redirect('/admin')
            else:
                return flash("Неверный логин или пароль")
        except Exception as e:
            print(e)
            return redirect("/error")
    return render_template("signin.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()  # вызываем функцию из flask-login
    return redirect("/index")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password = hashlib.sha224(password.encode()).hexdigest()
        new_user = User(email=email, username=username, password=password, role=2)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            flash("Виталя что-то ту не так")
        return redirect("/signin")
    return render_template("signup.html")


# Пользователь
@app.route('/account', methods=['POST', 'GET'])
def account():
    cur_user_fav_game = FavoriteGame.query.filter_by(user_id=current_user.id).all()
    cur_user_fav_game_ids = [fav_game.game_id for fav_game in cur_user_fav_game]

    # Используйте единственный запрос для извлечения всех объектов Game, связанных с избранными играми пользователя
    cur_user_games = Game.query.filter(or_(Game.id.in_(cur_user_fav_game_ids), Game.id.is_(None))).all()

    games_list = [[g.name_ru, str(g.id)] for g in cur_user_games]

    return render_template("account.html", games=games_list)



@app.route('/user/<username>')
def get_user(username):
    return f"Hello {username}"


# Игры
@app.route('/choose/<game>', methods=['POST', 'GET'])
def choose_game(game):
    game = Game.query.filter(Game.id == game).first()
    if game is None:
        return render_template("404.html")
    return render_template("game.html", game=game)


# Ошибки
@app.route('/thanks')
def thanks():
    return render_template("thanks.html")


@app.route('/del_session')
def del_session():
    session.pop('data', None)
    return redirect('/')


@app.route('/error')
def error():
    return render_template("error.html")


@app.route('/trap')
def trap():
    return render_template("trap.html")


@app.route('/not_found')
def not_found():
    return render_template("404.html")


@app.route('/add_to_favorites/<int:game_id>', methods=['GET', 'POST'])
@login_required
def add_to_favorites(game_id):
    game = Game.query.get(game_id)
    if game:
        favorite_game = FavoriteGame(user_id=current_user.id, game_id=game.id)
        db.session.add(favorite_game)
        db.session.commit()
        return redirect('/choose')

@app.route('/del_from_favorites/<int:game_id>', methods=['GET', 'POST'])
@login_required
def del_from_favorites(game_id):
    game = Game.query.get(game_id)
    if game:
        favorite_game = FavoriteGame.query.filter_by(user_id=current_user.id, game_id=game.id).first()
        if favorite_game:
            db.session.delete(favorite_game)
            db.session.commit()
        return redirect('/choose')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)