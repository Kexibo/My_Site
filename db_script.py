from app import app
from models import db, Game

with app.app_context():
    db.session.add(Game(name_en="Ogon I Voda",
                        name_ru="Огонь и вода",
                        tags="best",
                        url="https://html5.gamedistribution.com/56da8a54fe204845b34ccff750d4a60b/"))
    db.session.add(Game(name_en="igra-kopiya-majnkrafta",
                        name_ru="Minecraft",
                        tags="sandbox",
                        url="https://g.vseigru.net/11/igra-kopiya-majnkrafta"))
    db.session.add(Game(name_en="Terraria",
                        name_ru="Террария",
                        tags="sandbox",
                        url="https://g.vseigru.net/dasha1/196/1/igra-majnkraft-scratcharia.html"))
    db.session.add(Game(name_en="Gonki",
                        name_ru="Гонки",
                        tags="race",
                        url="https://g.vseigru.net/dasha1/igry-gonki/renegade_driver/"))
    db.session.add(Game(name_en="AmongUs",
                        name_ru="AmongUs",
                        tags="walk",
                        url="https://html5.gamedistribution.com/9abe6af0fbb440b98a3e24bf7fb0636a/?gdpr-tracking=0&gdpr-targeting=0&gdpr-third-party=0&gd_sdk_referrer_url=https://gamedistribution.com/games/impostor"))
    db.session.add(Game(name_en="Hunters vs Props Online",
                        name_ru="Прятки",
                        tags="hide",
                        url="https://html5.gamedistribution.com/a966f650eafc4e6986347b6440313fea/?gdpr-tracking=0&gdpr-targeting=0&gdpr-third-party=0&gd_sdk_referrer_url=https://gamedistribution.com/games/hunters-vs-props-online"))
    db.session.commit()
