from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    db.drop_all.__init__(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from blog.main.routes import main
    from blog.users.routes import users
    from blog.cars.routes import cars
    from blog.events.routes import events
    from blog.activities.routes import activities
    from blog.ccp.routes import ccp
    from blog.ccd.routes import ccd
    from blog.acp.routes import acp
    from blog.customers.routes import customers
    from blog.spares.routes import spares







    db.create_all(app=app)



    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(cars)
    app.register_blueprint(events)
    app.register_blueprint(activities)
    app.register_blueprint(ccp)
    app.register_blueprint(ccd)
    app.register_blueprint(acp)
    app.register_blueprint(customers)
    app.register_blueprint(spares)







    return app