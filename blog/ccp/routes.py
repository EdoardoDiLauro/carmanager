# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import CarCostProfile, Car, CarCostDriver, Event, CarCostDriverReset
from blog.ccp.forms import CcpForm, UpdateCcpForm
from blog.ccd.forms import CcdDashForm, CcdFormDash, CcdForm
from datetime import datetime, time
from sqlalchemy.sql import func

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
        return redirect(url_for('cars.car_ccp', car_id=car_id))
    return render_template('create_ccp.html', title='Add Car Cost Profile', form=form, legend='Add Car Cost Profile')

@ccp.route("/ccp/<int:car_id>/detail/<int:ccp_id>" , methods=['GET', 'POST'])
@login_required
def ccp_detail(ccp_id, car_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    ccp = CarCostProfile.query.get_or_404(ccp_id)
    if ccp.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    ccpform = UpdateCcpForm()
    newccdform = CcdForm()

    usedccd = db.session.query(CarCostDriver).filter(
        CarCostDriver.ccp.any(id=ccp.id)).filter(CarCostDriver.user_id == current_user.id)

    freeccd = db.session.query(CarCostDriver).filter(
        ~CarCostDriver.ccp.any(id=ccp.id)).filter(CarCostDriver.car_id == car_id)

    eventlist = db.session.query(Event).filter(Event.ccp_id == ccp.id)

    availdashform = CcdDashForm()
    useddashform = CcdDashForm()
    
    for cd in usedccd:
        cd_form = CcdFormDash()
        cd_form.spid = cd.id
        cd_form.nome = cd.name
        cd_form.value = cd.value
        cd_form.elapsed = cd.elapsed
        cd_form.avg = cd.avg
        cd_form.limit = cd.limit
        useddashform.sps.append_entry(cd_form)
        
    for cd in freeccd:
        cd_form = CcdFormDash()
        cd_form.spid = cd.id
        cd_form.nome = cd.name
        cd_form.value = cd.value
        cd_form.elapsed = cd.elapsed
        cd_form.avg = cd.avg
        cd_form.limit = cd.limit
        availdashform.sps.append_entry(cd_form)
        
    if availdashform.submitin.data:
        for data in availdashform.sps.entries:
            if data.select.data == 1:
                spmod = CarCostDriver.query.filter_by(id=data.spid.data).first()
                spmod.ccp.append(ccp)
                db.session.commit()
        flash('Car Cost Drivers successfully assigned', 'success')
        return redirect(url_for('ccp.ccp_detail', ccp_id=ccp_id, car_id=car_id))

    if useddashform.submitoff.data:
        for data in useddashform.sps.entries:
            if data.select.data == 1:
                spmod = CarCostDriver.query.filter_by(id=data.spid.data).first()
                ccp.ccd.remove(spmod)
                db.session.commit()
        flash('Car Cost Drivers successfully discarded', 'success')
        return redirect(url_for('ccp.ccp_detail', ccp_id=ccp_id, car_id=car_id))
        
    if newccdform.validate_on_submit():
        new_ccd = CarCostDriver(name=newccdform.name.data, value=newccdform.value.data, initial=newccdform.elapsed.data, elapsed=newccdform.elapsed.data,limit=newccdform.limit.data, avg=newccdform.limit.data, car_id=car.id, user_id=current_user.id)
        new_ccd.ccp.append(ccp)
        db.session.add(new_ccd)
        db.session.commit()
        flash('New Car Cost Driver successfully added', 'success')
        return redirect(url_for('ccp.ccp_detail', ccp_id=ccp_id, car_id=car_id))

    if ccpform.validate() and ccpform.name.data and ccpform.notes.data and ccpform.submitupccp.data:
        ccp.name = ccpform.name.data
        ccp.notes = ccpform.notes.data
        db.session.commit()
        flash('Car Cost Profile successfully updated', 'success')
        return redirect(url_for('ccp.ccp_detail', ccp_id=ccp_id, car_id=car_id))
    elif request.method == 'GET':
        ccpform.name.data = ccp.name
        ccpform.notes.data = ccp.notes
    return render_template('ccp.html', title='Update Car Cost Profile', newccdform=newccdform,ccpform=ccpform, car=car, ccp=ccp, eventlist=eventlist, availspares=availdashform, usedspares=useddashform, legend='Update Car Cost Profile')

@ccp.route("/ccp/<int:car_id>/delete/<int:ccp_id>" , methods=['GET', 'POST'])
@login_required
def delete_ccp(ccp_id, car_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    ccp = CarCostProfile.query.get_or_404(ccp_id)
    if ccp.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    eventlist = db.session.query(Event).filter(Event.ccp_id == ccp.id)

    for event in eventlist:
        event.ccp_id = 0
        db.session.commit()

    db.session.remove(ccp)
    flash('Car Cost Driver successfully removed', 'success')
    return redirect(url_for('cars.car_ccp', ccp_id=ccp_id))

@ccp.route("/ccp/<int:car_id>/resets/<int:ccp_id>" , methods=['GET', 'POST'])
@login_required
def resets(ccp_id, car_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    ccp = CarCostProfile.query.get_or_404(ccp_id)
    if ccp.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    ccpform = UpdateCcpForm()


    ccds = db.session.query(CarCostDriver).filter(
        CarCostDriver.ccp.any(id=ccp.id)).filter(CarCostDriver.user_id == current_user.id)

    eventlist = db.session.query(Event).filter(Event.ccp_id == ccp.id)


    for ccd in ccds:
        ccdr =  db.session.query(CarCostDriverReset).filter(CarCostDriverReset.ccd_id==ccd.id)
        if ccdr: ccd.avg = db.session.query(func.avg(CarCostDriverReset.elapsed).label('average')).filter(CarCostDriverReset.ccd_id==ccd.id)
        else: ccd.avg = ccd.limit
        db.session.commit()

    if ccpform.validate() and ccpform.name.data and ccpform.notes.data and ccpform.submitupccp.data:
        ccp.name = ccpform.name.data
        ccp.notes = ccpform.notes.data
        db.session.commit()
        flash('Car Cost Profile successfully updated', 'success')
        return redirect(url_for('ccp.ccp_detail', ccp_id=ccp_id, car_id=car_id))
    elif request.method == 'GET':
        ccpform.name.data = ccp.name
        ccpform.notes.data = ccp.notes
    return render_template('ccdr_overview.html', car=car, ccds=ccds, ccp=ccp, ccpform=ccpform,eventlist=eventlist, legend='Update Car Cost Profile')



