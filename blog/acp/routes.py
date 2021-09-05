# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import ActivityCostProfile, Activity
from blog.acp.forms import AcpForm
from datetime import datetime, time

acp = Blueprint('acp', __name__)

@acp.route("/acp/new/<int:event_id>" , methods=['GET', 'POST'])
@login_required
def create_acp(event_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    form = AcpForm()

    if form.validate_on_submit():
        if form.notes.data : new_acp = ActivityCostProfile(name=form.name.data, notes=form.notes.data, user_id=current_user.id)
        else:new_acp = ActivityCostProfile(name=form.name.data, user_id=current_user.id)
        db.session.add(new_acp)
        db.session.commit()
        flash('New Activity Cost Profile successfully added', 'success')
        return redirect(url_for('events.event_detail', event_id=event_id))
    return render_template('create_acp.html', title='Add Activity Cost Profile', form=form, legend='Add Activity Cost Profile')