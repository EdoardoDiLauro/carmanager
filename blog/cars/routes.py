# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Car
from blog.cars.forms import CarForm
from datetime import datetime, time

cars = Blueprint('cars', __name__)

@cars.route("/car/new" , methods=['GET', 'POST'])
@login_required
def create_car():
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))
    form = CarForm()
    if form.validate_on_submit():
        if form.plate.data : new_car = Car(brand=form.brand.data, model=form.model.data, cat=form.cat.data, group=form.group.data,plate=form.plate.data, user_id=current_user.id)
        else:new_car = Car(brand=form.brand.data, model=form.model.data, cat=form.cat.data, group=form.group.data, user_id=current_user.id)
        db.session.add(new_car)
        db.session.commit()
        flash('New car successfully added', 'success')
        return redirect(url_for('cars.overview'))
    return render_template('create_car.html', title='Add Car', form=form, legend='Add Car')

@cars.route("/car/overview", methods=['GET', 'POST'])
@login_required
def overview():
    ps = Car.query.filter_by(user_id=current_user.id).order_by()

    return render_template('car_overview.html', carlist=ps)

@cars.route("/car/<int:car_id>/delete", methods=['GET','POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)
    db.session.delete(car)
    db.session.commit()
    flash('Car successfully removed', 'success')
    return redirect(url_for('cars.overview'))

@cars.route("/car/<int:car_id>", methods=['GET','POST'])
@login_required
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    return render_template('car.html', car=car)
