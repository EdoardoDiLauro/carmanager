# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from sqlalchemy import func

from blog import db
from blog.models import Car, Activity, Event, CarCostDriver, CarCostProfile
from blog.cars.forms import CarForm, UpdateCarForm
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
        if form.notes.data : new_car = Car(brand=form.brand.data, model=form.model.data, kmbuy=form.kmtot.data, chassis=form.chassis.data,notes=form.notes.data, user_id=current_user.id)
        else:new_car = Car(brand=form.brand.data, model=form.model.data, kmbuy=form.kmtot.data, chassis=form.chassis.data, user_id=current_user.id)
        db.session.add(new_car)
        db.session.commit()
        flash('New car successfully added', 'success')
        return redirect(url_for('cars.overview'))
    return render_template('create_car.html', title='Add Car', form=form, legend='Add Car')

@cars.route("/car/overview", methods=['GET', 'POST'])
@login_required
def overview():
    ps = Car.query.filter_by(user_id=current_user.id).order_by()

    for car in ps:
        res = Activity.query.with_entities(func.sum(Activity.kmssact).label("sum")).filter(Activity.car_id==car.id).first()
        if res.sum:
            car.kmtot = car.kmbuy + res.sum
            db.session.commit()

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

    ps = Event.query.filter_by(user_id=current_user.id, car_id=car_id).order_by()


    form = UpdateCarForm()
    if form.validate_on_submit():
        if form.notes.data :
            car.brand=form.brand.data
            car.model=form.model.data
            car.kmbuy=form.kmtot.data
            car.chassis=form.chassis.data
            car.notes=form.notes.data
        else:
            car.brand=form.brand.data
            car.model=form.model.data
            car.kmbuy=form.kmtot.data
            car.chassis=form.chassis.data
        db.session.commit()
        flash('Car successfully updated', 'success')
        return redirect(url_for('cars.car_detail', car_id=car_id))
    elif request.method == 'GET':
        form.brand.data=car.brand
        form.model.data=car.model
        form.kmtot.data=car.kmtot
        form.chassis.data=car.chassis
        form.notes.data=car.notes

    return render_template('car.html', car=car, form=form,legend="Car Details", eventlist=ps)


@cars.route("/car/<int:car_id>/ccp", methods=['GET','POST'])
@login_required
def car_ccp(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    ps = CarCostProfile.query.filter_by(user_id=current_user.id, car_id=car_id).order_by()

    form = UpdateCarForm()
    if form.validate_on_submit():
        if form.notes.data:
            car.brand = form.brand.data
            car.model = form.model.data
            car.kmbuy = form.kmtot.data
            car.chassis = form.chassis.data
            car.notes = form.notes.data
        else:
            car.brand = form.brand.data
            car.model = form.model.data
            car.kmbuy = form.kmtot.data
            car.chassis = form.chassis.data
        db.session.commit()
        flash('Car successfully updated', 'success')
        return redirect(url_for('cars.car_ccp', car_id=car_id))
    elif request.method == 'GET':
        form.brand.data = car.brand
        form.model.data = car.model
        form.kmtot.data = car.kmtot
        form.chassis.data = car.chassis
        form.notes.data = car.notes

    return render_template('car_ccp.html', car=car, form=form, legend="Car Details", ccplist=ps)