from blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


linksccd=db.Table('linksccd',
            db.Column('CarCostProfile_id', db.Integer, db.ForeignKey('CarCostProfile.id'), nullable=False),
            db.Column('CarCostDriver_id', db.Integer, db.ForeignKey('CarCostDriver.id'), nullable=False)
)

linksacd=db.Table('linksacd',
            db.Column('ActivityCostProfile_id', db.Integer, db.ForeignKey('ActivityCostProfile.id'), nullable=False),
            db.Column('ActivityCostDriver_id', db.Integer, db.ForeignKey('ActivityCostDriver.id'), nullable=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    onhold = db.Column(db.Boolean)

    def __repr__(self):
        return "User('{self.username}', '{self.email}')"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    kmtot = db.Column(db.Integer, nullable=False, default=0)
    chassis = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.String(200), nullable=True)
    events = db.relationship('Event')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Car ('{self.id}')"

class CarCostProfile(db.Model):
    __tablename__ = 'CarCostProfile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "CarCostProfile ('{self.id}')"

class CarCostDriver(db.Model):
    __tablename__ = 'CarCostDriver'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    elapsed = db.Column(db.Float, nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    ccp = db.relationship('CarCostProfile', secondary=linksccd, backref='ccps', lazy=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "CarCostDriver ('{self.id}')"

class CarCostDriverReset(db.Model):
    __tablename__ = 'CarCostDriverReset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    elapsed = db.Column(db.Float, nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    resdate = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    ccd_id = db.Column(db.Integer, db.ForeignKey('CarCostDriver.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "CarCostDriverReset ('{self.id}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    kmssth = db.Column(db.Integer, nullable=False)
    kmssact = db.Column(db.Integer, nullable=True)
    ccp_id = db.Column(db.Integer, db.ForeignKey('CarCostProfile.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Event ('{self.id}')"

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    kmssact = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(200), nullable=True)
    acp_id = db.Column(db.Integer, db.ForeignKey('ActivityCostProfile.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Activity ('{self.id}')"

class ActivityCostProfile(db.Model):
    __tablename__ = 'ActivityCostProfile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    acd = db.relationship('ActivityCostDriver', secondary=linksacd, backref='drivers', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "ActivityCostProfile ('{self.id}')"

class ActivityCostDriver(db.Model):
    __tablename__ = 'ActivityCostDriver'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    acp = db.relationship('ActivityCostProfile', secondary=linksacd, backref='acps', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "ActivityCostDriver ('{self.id}')"

class Spare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    isnew = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(200), nullable=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Spare ('{self.id}')"

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    regdate = db.Column(db.DateTime, nullable=False)
    totprice = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Invoice ('{self.id}')"

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Customer ('{self.id}')"





