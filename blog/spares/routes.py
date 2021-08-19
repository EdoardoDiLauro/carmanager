# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Spare, Car, Activity, CarCostProfile, Customer
from blog.spares.forms import SpareForm
from datetime import datetime, time

spares = Blueprint('spares', __name__)

@spares.route("/spare/new" , methods=['GET', 'POST'])
@login_required
def create_spare():
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))
    
    form = SpareForm()

    if form.validate_on_submit():
        if form.isnew.data == 1:
            if form.notes.data : new_spare = Spare(name=form.name.data, notes=form.notes.data, area=form.area.data, isnew=True,
                              price=form.price.data,
                              user_id=current_user.id)
            else: new_spare = Spare(name=form.name.data, area=form.area.data, isnew=True,
                              price=form.price.data,
                              user_id=current_user.id)
            db.session.add(new_spare)
            db.session.commit()
            flash('New spare part successfully added', 'success')
            return redirect(url_for('spares.overview'))
        else:
            if form.notes.data:
                new_spare = Spare(name=form.name.data, notes=form.notes.data, area=form.area.data, isnew=False,
                                  price=form.price.data,
                                  user_id=current_user.id)
            else:
                new_spare = Spare(name=form.name.data, area=form.area.data, isnew=False,
                                  price=form.price.data,
                                  user_id=current_user.id)
            db.session.add(new_spare)
            db.session.commit()
            flash('New spare part successfully added', 'success')
            return redirect(url_for('spares.overview'))
    return render_template('create_spare.html', title='Add Spare Part', form=form, legend='Add Spare Part')

