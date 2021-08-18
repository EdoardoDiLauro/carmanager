# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Event, Car, Activity, ActivityCostProfile
from blog.activities.forms import ActForm
from datetime import datetime, time

activities = Blueprint('activities', __name__)


@activities.route("/activity/<int:event_id>", methods=['GET','POST'])
@login_required
def add_act(event_id):
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
        new_act = Activity(name=form.name.data, type =form.type.data, kmssact=form.kmssth.data, acp_id=form.acp.data,
                          start=form.start.data,end=form.end.data, car_id=car.id, user_id=current_user.id, event_id=event.id)
        db.session.add(new_event)
        db.session.commit()
        flash('New activity successfully added', 'success')
        return redirect(url_for('events.event_detail', event_id=event_id))
    return render_template('add_act.html', title='Add Activity', form=form, legend='Add Activity', car=car, event=event)
