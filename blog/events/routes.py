# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Event, Car, Activity, CarCostProfile, Customer, CarCostDriver
from blog.events.forms import EventForm, UpdateEventForm
from datetime import datetime, time

events = Blueprint('events', __name__)

@events.route("/event/new/<int:car_id>" , methods=['GET', 'POST'])
@login_required
def create_event(car_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    form = EventForm()

    form.ccp.choices= [(-1," ")]+[(item.id, item.name) for item in db.session.query(CarCostProfile).filter(CarCostProfile.car_id==car.id)]


    if form.validate_on_submit() and form.ccp.data != -1:
        new_event = Event(name=form.name.data, kmssth =form.kmssth.data, kmssact=form.kmssth.data, ccp_id=form.ccp.data,
                          start=form.start.data, customer_id=0 ,end=form.end.data, car_id=car.id, user_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        flash('New event successfully added', 'success')
        return redirect(url_for('cars.car_detail', car_id=car_id))
    return render_template('create_event.html', title='Add Event', form=form, legend='Add Event', car=car)

@events.route("/event/overview/<int:car_id>", methods=['GET', 'POST'])
@login_required
def overview(car_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)

    ps = Event.query.filter_by(user_id=current_user.id, car_id=car_id).order_by()

    return render_template('event_overview.html', eventlist=ps, car=car)


@events.route("/event/<int:event_id>/delete", methods=['GET','POST'])
@login_required
def delete_event(event_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('event successfully removed', 'success')
    return redirect(url_for('events.overview'))

@events.route("/event/<int:event_id>", methods=['GET','POST'])
@login_required
def event_detail(event_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(event.car_id)
    if car.user_id != current_user.id:
        abort(403)

    ccp = CarCostProfile.query.get_or_404(event.ccp_id)
    if ccp.user_id != current_user.id:
        abort(403)

    acts = Activity.query.filter(Activity.event_id==event_id).order_by(Activity.start)

    event.totcostact=0
    event.kmssact=0
    event.totcostspares=0

    for act in acts:
        if act.totcostact: event.totcostact=event.totcostact+act.totcostact
        if act.totcostspares: event.totcostspares=event.totcostspares+act.totcostspares
        event.kmssact=event.kmssact+act.kmssact
        db.session.commit()

    usedccd = db.session.query(CarCostDriver).filter(
        CarCostDriver.ccp.any(id=ccp.id)).filter(CarCostDriver.user_id == current_user.id)

    ccp.perkm = 0

    for ccd in usedccd:
        perkm = ccd.value/ccd.limit
        ccp.perkm = ccp.perkm + perkm
        db.session.commit()

    event.totcostkm=ccp.perkm*event.kmssact
    db.session.commit()


    form = UpdateEventForm()

    form.ccp.choices= [(-1," ")]+[(item.id, item.name) for item in db.session.query(CarCostProfile).filter(CarCostProfile.car_id==car.id)]
    form.customer.choices = [(-1, " ")] + [(item.id, item.name) for item in
                                      db.session.query(Customer).filter(Customer.user_id == current_user.id)]
    if form.validate() and form.name.data and form.start.data and form.end.data and form.kmssth.data and form.ccp.data != -1:
        event.name = form.name.data
        event.start = form.start.data
        event.end = form.end.data
        event.kmssth = form.kmssth.data
        event.ccp_id = form.ccp.data
        event.customer_id = form.customer.data
        db.session.commit()
        flash('Event successfully updated', 'success')
        return redirect(url_for('events.event_detail', event_id=event_id))
    if form.validate() and form.name.data and form.start.data and form.end.data and form.kmssth.data and form.ccp.data != -1 and form.customer.data != -1 :
        event.name = form.name.data
        event.start = form.start.data
        event.end = form.end.data
        event.kmssth = form.kmssth.data
        event.ccp_id = form.ccp.data
        event.customer_id = form.customer.data
        db.session.commit()
        flash('Event successfully updated', 'success')
        return redirect(url_for('events.event_detail', event_id=event_id))
    elif request.method == 'GET':
        form.name.data = event.name
        form.start.data = event.start
        form.end.data = event.end
        form.kmssth.data = event.kmssth
        form.ccp.data = event.ccp_id
        form.customer.data = event.customer_id
    return render_template('event.html', event=event, form=form, legend='Update Event', car=car, acts=acts)

@events.route("/removeact/<int:event_id>/<int:activity_id>", methods=['GET','POST'])
@login_required
def remove_act(event_id, activity_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    act = Activity.query.get_or_404(activity_id)
    if act.user_id != current_user.id:
        abort(403)

    db.session.delete(act)
    db.session.commit()
    flash('Activity successfully removed', 'success')
    return redirect(url_for('events.event_detail', event_id=event_id))



