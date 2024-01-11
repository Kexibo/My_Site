"""
Скрипт добавляет администратора с захэшированным паролем в таблицу users
P.S: требуется в начале создать роли
"""

from app import db, app
from models import User
import hashlib

new_user = User(username="admin", email="admin@gmail.com", password=hashlib.sha224("admin".encode()).hexdigest(), role=1)
with app.app_context():
    db.session.add(new_user)
    db.session.commit()
