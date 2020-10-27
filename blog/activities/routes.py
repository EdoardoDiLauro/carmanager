# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Event, Car, Team, Activity, Cd, Cdtype
from blog.activities.forms import CdForm
from datetime import datetime, time

activities = Blueprint('activities', __name__)


@activities.route("/activity/<int:activity_id>", methods=['GET','POST'])
@login_required
def activity_detail(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.user_id != current_user.id:
        abort(403)

    event = Event.query.get_or_404(activity.event_id)
    car = Car.query.get_or_404(activity.car)
    cds = Cd.query.filter_by(act_id=activity_id, user_id=current_user.id)

    form = CdForm()

    form.type.choices = [(item.id, item.name) for item in db.session.query(Cdtype).filter(Cdtype.user_id == current_user.id)]

    if form.validate_on_submit():
        cdtype = Cdtype.query.get_or_404(form.type.data)
        if cdtype.isperkm == True:
            totcost = form.uncost.data * event.kmss
            cd = Cd(name=form.name.data, uncost = form.uncost.data, totcost=totcost, qty=1, user_id=current_user.id, event_id=event.id, type_id= cdtype.id )
        elif cdtype.isperkm == False:
            totcost = form.uncost.data * form.qty.data
            cd = Cd(name=form.name.data, uncost=form.uncost.data, totcost=totcost, qty=1, user_id=current_user.id,
                    event_id=event.id, type_id=cdtype.id)
        db.session.add(cd)
        db.session.commit()
        flash('New Cost Driver successfully added', 'success')
        return redirect(url_for('activities.activity_detail', activity_id=activity_id))

    return render_template('activity.html', activity=activity, event=event, car=car, cds=cds, form=form)
