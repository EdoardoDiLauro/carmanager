# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Event, Car, Team, Activity
from blog.events.forms import EventForm, UpdateEventForm, AddCarForm
from datetime import datetime, time

events = Blueprint('events', __name__)

@events.route("/event/new" , methods=['GET', 'POST'])
@login_required
def create_event():
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))
    form = EventForm()
    if form.validate_on_submit():
        if form.type.data == 0:
            new_event = Event(istest=True, name=form.name.data, year=form.year.data, kmss=form.kms.data, start=form.start.data,
                                    end=form.end.data, user_id=current_user.id)
        elif form.type.data == 1:
            new_event = Event(israce=True, name=form.name.data, year=form.year.data, kmss=form.kms.data,
                                    start=form.start.data,
                                    end=form.end.data, user_id=current_user.id)
        elif form.type.data == 2:
            new_event = Event(isrestore=True, name=form.name.data, year=form.year.data, kmss=form.kms.data,
                                    start=form.start.data,
                                    end=form.end.data, user_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        flash('New event successfully added', 'success')
        return redirect(url_for('events.overview'))
    return render_template('create_event.html', title='Add event', form=form, legend='Add event')

@events.route("/event/overview", methods=['GET', 'POST'])
@login_required
def overview():
    ps = Event.query.filter_by(user_id=current_user.id).order_by()

    return render_template('event_overview.html', eventlist=ps)


@events.route("/event/<int:event_id>/delete", methods=['GET','POST'])
@login_required
def delete_event(event_id):
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
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    form = UpdateEventForm()

    if form.validate():
        event.name = form.name.data
        event.start = form.start.data
        event.end = form.end.data
        event.year = form.year.data
        event.kmss = form.kms.data
        db.session.commit()
        flash('Event successfully updated', 'success')
        return redirect(url_for('events.event_detail', event_id=event_id))
    elif request.method == 'GET':
        form.name.data = event.name
        form.start.data = event.start
        form.end.data = event.end
        form.year.data = event.year
        form.kms.data = event.kmss
    return render_template('event.html', event=event, form=form)

@events.route("/event/<int:event_id>", methods=['GET','POST'])
@login_required
def add_car_to_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    form = AddCarForm()

    form.car.choices= [(-1," ")]+[(item.id, item.brand) for item in db.session.query(Car).filter(Car.user_id==current_user.id)]
    form.team.choices= [(-1," ")]+[(item.id, item.name) for item in db.session.query(Team).filter(Team.user_id==current_user.id)]

    if form.validate_on_submit() and form.car.data != -1:
        if form.team.data != -1:
            new_activity = Activity(user_id=current_user.id, event_id=event_id, car=form.car.data, team_id=form.team.data)
        else:
            new_activity = Activity(user_id=current_user.id, event_id=event_id, car=form.car.data)
        db.session.add(new_activity)
        db.session.commit()
        flash('Car assigned, new activity successfully added', 'success')
        return redirect(url_for('events.event_detail', event_id=event_id))

    return render_template('addcartoevent.html', event=event, form=form)
