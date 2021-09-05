# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from sqlalchemy import desc

from blog import db
from blog.models import Event, Car, Activity, ActivityCostProfile, ActivityCostDriver, Spare, CarCostProfile, CarCostDriver, CarCostDriverReset
from blog.activities.forms import ActForm, UpdateActForm
from blog.acp.forms import UpdateAcpForm
from blog.acd.forms import UpdateAcdForm, AcdForm, AcdDashForm, UpdateAcdFormDash
from blog.spares.forms import SpareFormDash, SpareDashForm
from datetime import datetime, time

activities = Blueprint('activities', __name__)


@activities.route("/activity/<int:event_id>", methods=['GET','POST'])
@login_required
def add_act(event_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(event.car_id)
    if car.user_id != current_user.id:
        abort(403)

    form = ActForm()

    form.acp.choices = [(-1, " ")] + [(item.id, item.name) for item in
                                      db.session.query(ActivityCostProfile).filter(ActivityCostProfile.user_id == current_user.id)]

    if form.validate_on_submit() and form.acp.data != -1:
        if form.notes.data: new_act = Activity(name=form.name.data, notes=form.notes.data, type =form.type.data, kmssact=form.kmssact.data, acp_id=form.acp.data,
                          start=form.start.data,end=form.end.data, car_id=car.id, user_id=current_user.id, event_id=event.id)
        else: new_act = Activity(name=form.name.data, type =form.type.data, kmssact=form.kmssth.data, acp_id=form.acp.data,
                          start=form.start.data,end=form.end.data, car_id=car.id, user_id=current_user.id, event_id=event.id)
        db.session.add(new_act)
        db.session.commit()
        flash('New activity successfully added', 'success')
        return redirect(url_for('events.event_detail', event_id=event_id))
    return render_template('add_act.html', title='Add Activity', form=form, legend='Add Activity', car=car, event=event)


@activities.route("/activity/<int:act_id>/detail", methods=['GET','POST'])
@login_required
def detail(act_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    act = Activity.query.get_or_404(act_id)
    if act.user_id != current_user.id:
        abort(403)

    event = Event.query.get_or_404(act.event_id)
    if event.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(event.car_id)
    if car.user_id != current_user.id:
        abort(403)

    form = UpdateActForm()

    form.acp.choices = [(-1, " ")] + [(item.id, item.name) for item in
                                      db.session.query(ActivityCostProfile).filter(
                                          ActivityCostProfile.user_id == current_user.id)]

    if form.validate() and form.name.data and form.start.data and form.end.data and form.type.data and form.kmssact.data and form.acp.data != -1:
        act.name = form.name.data
        act.start = form.start.data
        act.end = form.end.data
        act.type = form.type.data
        act.kmssact = form.kmssact.data
        act.acp_id = form.acp.data
        db.session.commit()
        flash('Activity successfully updated', 'success')
        return redirect(url_for('activities.detail', act_id=act_id))
    if form.validate() and form.name.data and form.start.data and form.end.data and form.type.data and form.kmssact.data and form.acp.data != -1 and form.notes.data :
        act.name = form.name.data
        act.start = form.start.data
        act.end = form.end.data
        act.type = form.type.data
        act.kmssact = form.kmssact.data
        act.acp_id = form.acp.data
        act.notes = form.notes.data
        db.session.commit()
        flash('Activity successfully updated', 'success')
        return redirect(url_for('activities.detail', act_id=act_id))
    elif request.method == 'GET':
        form.name.data = act.name
        form.start.data = act.start
        form.end.data = act.end
        form.type.data = act.type
        form.kmssact.data = act.kmssact
        form.acp.data = act.acp_id
        form.notes.data = act.notes
    return render_template('activity.html', act=act, event=event, form=form, legend='Update Activity', car=car)

@activities.route("/activity/<int:act_id>/acp", methods=['GET','POST'])
@login_required
def alter_acp(act_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    act = Activity.query.get_or_404(act_id)
    if act.user_id != current_user.id:
        abort(403)

    event = Event.query.get_or_404(act.event_id)
    if event.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(event.car_id)
    if car.user_id != current_user.id:
        abort(403)

    acp = ActivityCostProfile.query.get_or_404(act.acp_id)
    if acp.user_id != current_user.id:
        abort(403)

    form = UpdateActForm()
    acpform = UpdateAcpForm()
    dashform = AcdDashForm()
    newacdform = AcdForm()

    form.acp.choices = [(-1, " ")] + [(item.id, item.name) for item in
                                      db.session.query(ActivityCostProfile).filter(
                                          ActivityCostProfile.user_id == current_user.id)]

    cds = ActivityCostDriver.query.filter(ActivityCostDriver.acp.any(id=acp.id))

    for cd in cds:
        cd_form = UpdateAcdFormDash()
        cd_form.cdid = cd.id
        cd_form.nome = cd.name
        cd_form.value = cd.value
        dashform.cds.append_entry(cd_form)

    if dashform.submitacddf.data:
        for data in dashform.cds.entries:
            cdmod = ActivityCostDriver.query.filter_by(id=data.cdid.data).first()
            cdmod.name = data.nome.data
            cdmod.value = data.value.data
            db.session.commit()
        flash('Activity Cost Drivers successfully updated', 'success')
        return redirect(url_for('activities.alter_acp', act_id=act_id))
        
    if newacdform.validate_on_submit():
        new_acd = ActivityCostDriver(name=newacdform.name.data, value=newacdform.value.data, user_id=current_user.id)
        new_acd.acp.append(acp)
        db.session.add(new_acd)
        db.session.commit()
        flash('New Activity Cost Driver successfully added', 'success')
        return redirect(url_for('activities.alter_acp', act_id=act_id))


    if acpform.validate_on_submit():
        if acpform.name.data: acp.name = acpform.name.data
        if acpform.notes.data: act.notes = form.notes.data
        db.session.commit()
        flash('Activity Cost Profile successfully updated', 'success')
        return redirect(url_for('activities.alter_acp', act_id=act_id))

    if acp and request.method == 'GET':
        acpform.name.data = acp.name
        acpform.notes.data = acp.notes

    if form.validate() and form.name.data and form.start.data and form.end.data and form.type.data and form.kmssact.data and form.acp.data != -1:
        act.name = form.name.data
        act.start = form.start.data
        act.end = form.end.data
        act.type = form.type.data
        act.kmssact = form.kmssact.data
        act.acp_id = form.acp.data
        db.session.commit()
        flash('Activity successfully updated', 'success')
        return redirect(url_for('activities.alter_acp', act_id=act_id))
    if form.validate() and form.name.data and form.start.data and form.end.data and form.type.data and form.kmssact.data and form.acp.data != -1 and form.notes.data:
        act.name = form.name.data
        act.start = form.start.data
        act.end = form.end.data
        act.type = form.type.data
        act.kmssact = form.kmssact.data
        act.acp_id = form.acp.data
        act.notes = form.notes.data
        db.session.commit()
        flash('Activity successfully updated', 'success')
        return redirect(url_for('activities.alter_acp', act_id=act_id))
    elif request.method == 'GET':
        form.name.data = act.name
        form.start.data = act.start
        form.end.data = act.end
        form.type.data = act.type
        form.kmssact.data = act.kmssact
        form.acp.data = act.acp_id
        form.notes.data = act.notes
    return render_template('activity_acp.html', act=act, event=event, acpform=acpform, form=form, dashform=dashform,newacdform=newacdform, title='Update Activity', car=car, acp=acp)

@activities.route("/activity/<int:act_id>/spare", methods=['GET','POST'])
@login_required
def use_spare(act_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    act = Activity.query.get_or_404(act_id)
    if act.user_id != current_user.id:
        abort(403)

    event = Event.query.get_or_404(act.event_id)
    if event.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(event.car_id)
    if car.user_id != current_user.id:
        abort(403)

    usedspares = db.session.query(Spare).filter(
                                          Spare.activity_id == act_id, Spare.user_id==current_user.id)

    availablespares = db.session.query(Spare).filter(
                                          Spare.activity_id == 0, Spare.user_id==current_user.id)

    form = UpdateActForm()
    availdashform = SpareDashForm()
    useddashform = SpareDashForm()

    act.totcostspares = 0
    db.session.commit()

    form.acp.choices = [(-1, " ")] + [(item.id, item.name) for item in
                                      db.session.query(ActivityCostProfile).filter(
                                          ActivityCostProfile.user_id == current_user.id)]
    
    for sp in availablespares:
        sp_form = SpareFormDash()
        sp_form.spid = sp.id
        sp_form.nome =sp.name
        sp_form.isnew = sp.isnew
        sp_form.price = sp.price
        sp_form.notes = sp.notes
        availdashform.sps.append_entry(sp_form)

    for sp in usedspares:
        sp_form = SpareFormDash()
        sp_form.spid = sp.id
        sp_form.nome =sp.name
        sp_form.isnew = sp.isnew
        sp_form.price = sp.price
        sp_form.notes = sp.notes
        useddashform.sps.append_entry(sp_form)
        act.totcostspares = act.totcostspares + sp.price
        db.session.commit()

    if availdashform.submit.data:
        for data in availdashform.sps.entries:
            if data.select.data == 1:
                spmod = Spare.query.filter_by(id=data.spid.data).first()
                spmod.activity_id = act_id
                db.session.commit()
        flash('Spare Parts successfully assigned', 'success')
        return redirect(url_for('activities.use_spare', act_id=act_id))

    if useddashform.submitoff.data:
        for data in useddashform.sps.entries:
            if data.select.data == 1:
                spmod = Spare.query.filter_by(id=data.spid.data).first()
                spmod.activity_id = 0
                db.session.commit()
        flash('Spare Parts successfully discarded', 'success')
        return redirect(url_for('activities.use_spare', act_id=act_id))

    if form.validate() and form.name.data and form.start.data and form.end.data and form.type.data and form.kmssact.data and form.acp.data != -1:
        act.name = form.name.data
        act.start = form.start.data
        act.end = form.end.data
        act.type = form.type.data
        act.kmssact = form.kmssact.data
        act.acp_id = form.acp.data
        db.session.commit()
        flash('Activity successfully updated', 'success')
        return redirect(url_for('activities.use_spare', act_id=act_id))
    if form.validate() and form.name.data and form.start.data and form.end.data and form.type.data and form.kmssact.data and form.acp.data != -1 and form.notes.data:
        act.name = form.name.data
        act.start = form.start.data
        act.end = form.end.data
        act.type = form.type.data
        act.kmssact = form.kmssact.data
        act.acp_id = form.acp.data
        act.notes = form.notes.data
        db.session.commit()
        flash('Activity successfully updated', 'success')
        return redirect(url_for('activities.use_spare', act_id=act_id))
    elif request.method == 'GET':
        form.name.data = act.name
        form.start.data = act.start
        form.end.data = act.end
        form.type.data = act.type
        form.kmssact.data = act.kmssact
        form.acp.data = act.acp_id
        form.notes.data = act.notes
    return render_template('activity_spare.html', act=act, event=event, form=form, availspares=availdashform, usedspares=useddashform, legend='Update Activity', car=car)

@activities.route("/activity/<int:act_id>/res", methods=['GET','POST'])
@login_required
def res_cd(act_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    act = Activity.query.get_or_404(act_id)
    if act.user_id != current_user.id:
        abort(403)

    event = Event.query.get_or_404(act.event_id)
    if event.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(event.car_id)
    if car.user_id != current_user.id:
        abort(403)

    ccp = CarCostProfile.query.get_or_404(event.ccp_id)
    if ccp.user_id != current_user.id:
        abort(403)

    ccds = CarCostDriver.query.filter(CarCostDriver.ccp.any(id=ccp.id))

    for ccd in ccds:
        lastres = CarCostDriverReset.query.filter_by(idres=ccd.id).order_by(desc(CarCostDriverReset.resdate)).first()
        elapsed = 0
        if lastres: elacts = db.session.query(Activity).filter(Activity.user_id == current_user.id).filter(Activity.start>lastres.resdate).filter(Activity.end<=act.end).filter(Activity.car_id==car.id)
        else: elacts = db.session.query(Activity).filter(Activity.end<=act.end).filter(Activity.user_id == current_user.id).filter(Activity.car_id==car.id)

        for activity in elacts:
            ev = Event.query.get_or_404(activity.event_id)
            cp = CarCostProfile.query.get_or_404(ev.ccp_id)
            if ccd in cp.ccd:
                elapsed = elapsed + activity.kmssact

        if lastres:
            ccd.elapsed = elapsed
            if lastres.activity_id == act_id: ccd.elapsed = 0
        else: ccd.elapsed = elapsed + ccd.initial
        db.session.commit()

    form = UpdateActForm()

    form.acp.choices = [(-1, " ")] + [(item.id, item.name) for item in
                                      db.session.query(ActivityCostProfile).filter(
                                          ActivityCostProfile.user_id == current_user.id)]

    if form.validate() and form.name.data and form.start.data and form.end.data and form.type.data and form.kmssact.data and form.acp.data != -1:
        act.name = form.name.data
        act.start = form.start.data
        act.end = form.end.data
        act.type = form.type.data
        act.kmssact = form.kmssact.data
        act.acp_id = form.acp.data
        db.session.commit()
        flash('Activity successfully updated', 'success')
        return redirect(url_for('activities.res_cd', act_id=act_id))
    if form.validate() and form.name.data and form.start.data and form.end.data and form.type.data and form.kmssact.data and form.acp.data != -1 and form.notes.data:
        act.name = form.name.data
        act.start = form.start.data
        act.end = form.end.data
        act.type = form.type.data
        act.kmssact = form.kmssact.data
        act.acp_id = form.acp.data
        act.notes = form.notes.data
        db.session.commit()
        flash('Activity successfully updated', 'success')
        return redirect(url_for('activities.res_cd', act_id=act_id))
    elif request.method == 'GET':
        form.name.data = act.name
        form.start.data = act.start
        form.end.data = act.end
        form.type.data = act.type
        form.kmssact.data = act.kmssact
        form.acp.data = act.acp_id
        form.notes.data = act.notes

    return render_template('activity_res.html', act=act, event=event, ccp=ccp, form=form, ccds=ccds, legend='Restore Car Cost Drivers', car=car)


@activities.route("/activity/<int:act_id>/totcalc", methods=['GET','POST'])
@login_required
def calc_totcostact(act_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    act = Activity.query.get_or_404(act_id)
    if act.user_id != current_user.id:
        abort(403)

    acp = ActivityCostProfile.query.get_or_404(act.acp_id)
    if acp.user_id != current_user.id:
        abort(403)

    cds = ActivityCostDriver.query.filter(ActivityCostDriver.acp.any(id=acp.id))


    act.totcostact = 0
    db.session.commit()

    for acd in cds:
        act.totcostact = act.totcostact + acd.value
        db.session.commit()

    flash('Activity total cost successfully updated', 'success')
    return redirect(url_for('activities.alter_acp', act_id=act_id))


