# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from sqlalchemy.sql import func
from blog import db
from blog.models import Event, Car, Activity, ActivityCostProfile, ActivityCostDriver, Spare, CarCostDriver, CarCostDriverReset
from blog.ccdr.forms import CcdrForm
from blog.spares.forms import SpareFormDash, SpareDashForm
from datetime import datetime, time

ccdr = Blueprint('ccdr', __name__)


@ccdr.route("/activity/<int:act_id>/<int:ccd_id>", methods=['GET','POST'])
@login_required
def add_ccdr(act_id, ccd_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    act = Activity.query.get_or_404(act_id)
    if act.user_id != current_user.id:
        abort(403)

    ccd = CarCostDriver.query.get_or_404(ccd_id)
    if ccd.user_id != current_user.id:
        abort(403)

    form = CcdrForm()

    usedspares = db.session.query(Spare).filter(
        Spare.activity_id == act_id, Spare.user_id == current_user.id)

    availablespares = db.session.query(Spare).filter(
        Spare.activity_id == 0, Spare.user_id == current_user.id)

    availdashform = SpareDashForm()
    useddashform = SpareDashForm()

    for sp in availablespares:
        sp_form = SpareFormDash()
        sp_form.spid = sp.id
        sp_form.nome = sp.name
        sp_form.isnew = sp.isnew
        sp_form.price = sp.price
        sp_form.notes = sp.notes
        availdashform.sps.append_entry(sp_form)

    for sp in usedspares:
        sp_form = SpareFormDash()
        sp_form.spid = sp.id
        sp_form.nome = sp.name
        sp_form.isnew = sp.isnew
        sp_form.price = sp.price
        sp_form.notes = sp.notes
        useddashform.sps.append_entry(sp_form)

    if availdashform.submit.data:
        for data in availdashform.sps.entries:
            if data.select.data == 1:
                spmod = Spare.query.filter_by(id=data.spid.data).first()
                spmod.activity_id = act_id
                db.session.commit()
        flash('Spare Parts successfully assigned', 'success')
        return redirect(url_for('ccdr.add_ccdr', act_id=act_id, ccd_id=ccd_id))

    if useddashform.submitoff.data:
        for data in useddashform.sps.entries:
            if data.select.data == 1:
                spmod = Spare.query.filter_by(id=data.spid.data).first()
                spmod.activity_id = 0
                db.session.commit()
        flash('Spare Parts successfully discarded', 'success')
        return redirect(url_for('ccdr.add_ccdr', act_id=act_id, ccd_id=ccd_id))

    if form.validate_on_submit():
        new_ccdr = CarCostDriverReset(name=ccd.name, idres=ccd.id, value=ccd.value, elapsed=ccd.elapsed, limit=ccd.limit, resdate=act.end, notes=form.notes.data, activity_id=act_id, ccd_id=ccd_id, user_id=current_user.id)
        db.session.add(new_ccdr)
        ccd.elapsed = 0
        db.session.commit()
        flash('Cost Driver Reset performed', 'success')
        return redirect(url_for('activities.res_cd', act_id=act_id))
    return render_template('ccdr.html', act=act, form=form, availspares=availdashform, usedspares=useddashform, legend='Car Cost Driver Restore')

@ccdr.route("/ccdr/overview/car_id", methods=['GET','POST'])
@login_required
def overview(car_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    ccds = CarCostDriver.query.filter_by(car_id=car_id)

    for ccd in ccds:
        ccd.avg = db.session.query(func.avg(CarCostDriverReset.elapsed).label('average')).filter(CarCostDriverReset.ccd_id==ccd.id)

    return render_template('ccdr_overview.html', car=car, ccds=ccds)
