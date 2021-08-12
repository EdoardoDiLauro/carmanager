# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import CarCostProfile, Car
from blog.ccp.forms import CcpForm
from datetime import datetime, time

ccp = Blueprint('ccp', __name__)

@ccp.route("/ccp/<int:car_id>/new" , methods=['GET', 'POST'])
@login_required
def create_ccp(car_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    form = CcpForm()

    if form.validate_on_submit():
        if form.notes.data : new_ccp = CarCostProfile(name=form.name.data, notes=form.notes.data, car_id=car.id, user_id=current_user.id)
        else:new_ccp = CarCostProfile(name=form.name.data, car_id=car.id, user_id=current_user.id)
        db.session.add(new_ccp)
        db.session.commit()
        flash('New Car Cost Profile successfully added', 'success')
        return redirect(url_for('cars.car_detail', car_id=car_id))
    return render_template('create_ccp.html', title='Add Car Cost Profile', form=form, legend='Add Car Cost Profile')