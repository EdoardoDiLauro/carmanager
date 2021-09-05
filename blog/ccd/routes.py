# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import CarCostProfile, Car, CarCostDriver, CarCostDriverReset
from blog.ccd.forms import CcdForm, UpdateCcdForm
from datetime import datetime, time

ccd = Blueprint('ccd', __name__)

@ccd.route("/ccd/<int:ccp_id>/<int:car_id>/new" , methods=['GET', 'POST'])
@login_required
def create_ccd(car_id, ccp_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    ccp = CarCostProfile.query.get_or_404(ccp_id)
    if ccp.user_id != current_user.id:
        abort(403)

    form = CcdForm()

    if form.validate_on_submit():
        if form.notes.data : new_ccd = CarCostDriver(name=form.name.data, value=form.value.data, elapsed=form.elapsed.data, limit=form.limit.data,  notes=form.notes.data, car_id=car.id, user_id=current_user.id)
        else:new_ccd = CarCostDriver(name=form.name.data, value=form.value.data, elapsed=form.elapsed.data, limit=form.limit.data, car_id=car.id, user_id=current_user.id)
        new_ccd.ccp.append(ccp)
        db.session.add(new_ccd)
        db.session.commit()
        flash('New Car Cost Driver successfully added', 'success')
        return redirect(url_for('cars.car_detail', car_id=car_id))
    return render_template('create_ccd.html', title='Add Car Cost Driver', form=form, legend='Add Car Cost Driver')

@ccd.route("/ccd/<int:ccd_id>" , methods=['GET', 'POST'])
@login_required
def ccd_detail(ccd_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    ccd = CarCostDriver.query.get_or_404(ccd_id)
    if ccd.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(ccd.car_id)
    if car.user_id != current_user.id:
        abort(403)

    ccdrs = db.session.query(CarCostDriverReset).filter_by(ccd_id=ccd_id)

    form = UpdateCcdForm()

    if form.validate_on_submit():
        ccd.name =form.name.data
        ccd.value = form.value.data
        ccd.elapsed = form.elapsed.data
        ccd.avg = form.avg.data
        ccd.limit = form.limit.data
        db.session.commit()
        flash('Car Cost Driver successfully updated', 'success')
        return redirect(url_for('ccd.ccd_detail', ccd_id=ccd_id))
    elif request.method == 'GET':
        form.name.data = ccd.name
        form.value.data = ccd.value
        form.elapsed.data = ccd.elapsed
        form.avg.data = ccd.avg
        form.limit.data = ccd.limit
    return render_template('ccd.html', car=car, ccd=ccd, ccdrs=ccdrs, form=form, legend='Update Car Cost Driver')


