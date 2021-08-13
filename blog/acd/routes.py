# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import ActivityCostProfile, Activity, ActivityCostDriver
from blog.acd.forms import AcdForm
from datetime import datetime, time

acd = Blueprint('acd', __name__)

@acd.route("/acd/<int:acp_id>/new" , methods=['GET', 'POST'])
@login_required
def create_acd(acp_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    acp = ActivityCostProfile.query.get_or_404(acp_id)
    if acp.user_id != current_user.id:
        abort(403)

    form = AcdForm()

    if form.validate_on_submit():
        if form.notes.data : new_acd = ActivityCostDriver(name=form.name.data, value=form.value.data, notes=form.notes.data, user_id=current_user.id)
        else:new_acd = ActivityCostDriver(name=form.name.data, value=form.value.data, user_id=current_user.id)
        new_acd.acp.append(acp)
        db.session.add(new_acd)
        db.session.commit()
        flash('New Activity Cost Driver successfully added', 'success')
        return redirect(url_for('events.overview'))
    return render_template('create_acd.html', title='Add Activity Cost Driver', form=form, legend='Add Activity Cost Driver')