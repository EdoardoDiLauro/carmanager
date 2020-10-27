import os

from flask import render_template, url_for, flash, redirect, request, Blueprint, app, abort, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from blog.models import User
from blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                              RequestResetForm, ResetPasswordForm, ContactForm, UserForm, UserValidationForm)
from blog.users.utils import save_picture, send_reset_email

from blog import db, bcrypt

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        pass1 = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user=User(username=form.username.data,email=form.email.data, name=form.name.data, surname=form.surname.data ,password=pass1, onhold=False)
        # change before deployment
        db.session.add(new_user)
        db.session.commit()
        flash('Succesful account creation', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.onhold == 1:
                flash('Login error, check account status', 'danger')
                return redirect(url_for('users.login'))
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        elif form.email.data=='admin@carmanager.com' and form.password.data=='admin':
            return redirect(url_for('users.adminpanel', admin=1))
        else:
            flash('Login error check credentials', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/adminpanel", methods=['GET', 'POST'])
def adminpanel():
    if not request.values.get('admin'):
        return redirect(url_for('main.home'))

    teamform= UserValidationForm()
    userlist=User.query.all()

    for r in userlist:
        rform= UserForm()
        rform.rid=r.id
        rform.nome=r.username
        if r.onhold==True:
            rform.status = "On Hold"
        else: rform.status= "Validated"


        teamform.users.append_entry(rform)

    if teamform.submit.data:
        for data in teamform.users.entries:
            r = User.query.filter_by(id=data.rid.data).first()
            if data.onhold.data == 0:
                r.onhold = False
            elif data.onhold.data == 1:
                r.onhold = True

            db.session.commit()


        return redirect(url_for('users.adminpanel', admin=1))

    return render_template('adminpanel.html', title='Users Management', legend='Users Management', form=teamform)



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        db.session.commit()
        flash('Succesfully updated informations', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.surname.data = current_user.surname
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Reset password procedure initiated, check your mailbox.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Updated password! Access granted', 'success')
        return redirect(url_for('Users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route("/forcelogin/<int:id>", methods=['GET', 'POST'])
def forcelogin(id):
    user = User.query.filter_by(id=id).first()
    login_user(user, remember=False)
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('users.account'))