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
                              user_id=current_user.id,activity_id=0, invoice_id=0)
            else: new_spare = Spare(name=form.name.data, area=form.area.data, isnew=True,
                              price=form.price.data,
                              user_id=current_user.id, activity_id=0, invoice_id=0)
            db.session.add(new_spare)
            db.session.commit()
            flash('New spare part successfully added', 'success')
            return redirect(url_for('spares.overview'))
        else:
            if form.notes.data:
                new_spare = Spare(name=form.name.data, notes=form.notes.data, area=form.area.data, isnew=False,
                                  price=form.price.data,
                                  user_id=current_user.id, activity_id=0, invoice_id=0)
            else:
                new_spare = Spare(name=form.name.data, area=form.area.data, isnew=False,
                                  price=form.price.data,
                                  user_id=current_user.id, activity_id=0, invoice_id=0)
            db.session.add(new_spare)
            db.session.commit()
            flash('New spare part successfully added', 'success')
            return redirect(url_for('spares.overview'))
    return render_template('create_spare.html', title='Add Spare Part', form=form, legend='Add Spare Part')

@spares.route("/spare/overview" , methods=['GET', 'POST'])
@login_required
def overview():
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    psn = Spare.query.filter_by(user_id=current_user.id, activity_id =0).order_by()
    psu = Spare.query.filter_by(user_id=current_user.id).filter(Spare.activity_id !=0).order_by()


    return render_template('spare_overview.html', newsparelist=psn , usedsparelist=psu)


@spares.route("/spare/<int:spare_id>" , methods=['GET', 'POST'])
@login_required
def spare_detail(spare_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    spare = Spare.query.get_or_404(spare_id)
    if spare.user_id != current_user.id:
        abort(403)

    form = SpareForm()

    if form.validate_on_submit():
        spare.area = form.area.data
        spare.name = form.name.data
        spare.isnew = form.isnew.data
        spare.price = form.price.data
        spare.notes = form.notes.data
        db.session.commit()
        flash('Spare successfully updated', 'success')
        return redirect(url_for('spares.overview', spare_id=spare_id))
    elif request.method == 'GET':
        form.area.data = spare.area
        form.name.data = spare.name
        form.isnew.data = spare.isnew
        form.price.data = spare.price
        form.notes.data = spare.notes
    return render_template('spare.html', form=form, legend='Update Spare')

    
@spares.route("/spare/<int:spare_id>/delete", methods=['GET','POST'])
@login_required
def delete_spare(spare_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    spare = Spare.query.get_or_404(spare_id)
    if spare.user_id != current_user.id:
        abort(403)
    db.session.delete(spare)
    db.session.commit()
    flash('Spare part successfully removed', 'success')
    return redirect(url_for('spares.overview'))