from blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


linksas=db.Table('linksas',
            db.Column('sponsor_id', db.Integer, db.ForeignKey('sponsorship.id'), nullable=False),
            db.Column('activity_id', db.Integer, db.ForeignKey('activity.id'), nullable=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), nullable=False)
    onhold = db.Column(db.Boolean)

    def __repr__(self):
        return "User('{self.username}', '{self.email}')"

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, nullable=True)
    totcost = db.Column(db.Float, nullable=True)
    driver = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=True)
    codriver = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=True)
    car = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    sponsors = db.relationship('Sponsorship', secondary=linksas, backref='acts', lazy=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Activity ('{self.id}')"


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    group = db.Column(db.String(30), nullable=False)
    cat = db.Column(db.String(30), nullable=False)
    plate = db.Column(db.String(50), nullable=True)
    tp = db.Column(db.String(50), nullable=True)
    hom = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Car ('{self.id}')"

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Team ('{self.id}')"

class Cdtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isperkm = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(200), nullable=False)
    group = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Cdtype ('{self.id}')"

class Doctype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    entity = db.Column(db.String(200), nullable=False)
    ent_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Doctype ('{self.id}')"


class Cd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    uncost = db.Column(db.Float, nullable=False)
    totcost = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    act_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('cdtype.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Cd ('{self.id}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    istest=db.Column(db.Boolean, default=False)
    israce=db.Column(db.Boolean, default=False)
    isrestore=db.Column(db.Boolean, default=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    kmss = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Event ('{self.id}')"

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), nullable=False)
    lic = db.Column(db.Integer, nullable=False)
    asn = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Driver ('{self.id}')"

class Sponsorship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    sponsor = db.Column(db.String(200), nullable=False)
    driver = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=True)
    car = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=True)
    sponsored = db.relationship('Activity', secondary=linksas, backref='partners', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Sponsorship ('{self.id}')"

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Component ('{self.id}')"



