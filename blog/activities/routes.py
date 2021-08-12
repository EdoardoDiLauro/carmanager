# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Event, Car, Activity
from blog.activities.forms import CdForm, SponsorForm, RaceSponsorForm
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
    programsponsors = ProgramSponsorship.query.filter_by(user_id=current_user.id).filter(ProgramSponsorship.sponsored.any(id==activity_id))

    sponsorform = SponsorForm()
    racesponsorform = RaceSponsorForm()
    form = CdForm()

    sponsorform.sponsor.choices = [(sp.id, sp.name) for sp in db.session.query(ProgramSponsorship).filter(Team.user_id==current_user.id & ProgramSponsorship.sponsored.any(id!=activity_id))]

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

    if sponsorform.validate_on_submit():
        sponsor = ProgramSponsorship.query.get_or_404(sponsorform.sponsor.data)
        db.session.commit()
        flash('Race successfully binded to Program Sponsor', 'success')
        return redirect(url_for('activities.activity_detail', activity_id=activity_id))

    if racesponsorform.validate_on_submit():
        new_sponsor = RaceSponsorship(user_id=current_user.id)
        db.session.add(new_sponsor)
        db.session.commit()
        flash('New Race Sponsor successfully added', 'success')
        return redirect(url_for('activities.activity_detail', activity_id=activity_id))




    return render_template('activity.html', activity=activity, event=event, car=car, cds=cds, form=form, sponsors=programsponsors, sf=sponsorform, rf=racesponsorform)
