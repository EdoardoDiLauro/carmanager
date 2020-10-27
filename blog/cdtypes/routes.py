# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from sqlalchemy import func

from blog import db
from blog.models import Event, Car, Team, Activity, Cd, Cdtype
from blog.cdtypes.forms import CdTypeForm
from datetime import datetime, time

cdtypes = Blueprint('cdtypes', __name__)


@cdtypes.route("/cdtype/new" , methods=['GET', 'POST'])
@login_required
def create_cdtype():
    form = CdTypeForm()

    form.exgroup.choices = [(-1," ")]+[(item.id, item.group) for item in db.session.query(func.max(Cdtype)).group_by(Cdtype.group).all().filter(Cdtype.user_id==current_user.id)]

    if form.validate_on_submit():
        if form.exgroup.data != -1 and form.isperkm.data == 1:
            exref = Cdtype.query.get_or_404(id=form.exgroup.data)
            cdtype = Cdtype(name=form.name.data, isperkm=True, group=exref.group, user_id=current_user.id)
        elif form.exgroup.data != -1 and form.isperkm.data == 0:
            exref = Cdtype.query.get_or_404(id=form.exgroup.data)
            cdtype = Cdtype(name=form.name.data, isperkm=False, group=exref.group, user_id=current_user.id)
        elif form.exgroup.data == -1 and form.isperkm.data == 0 and form.newgroup.data:
            cdtype = Cdtype(name=form.name.data, isperkm=False, group=form.newgroup.data, user_id=current_user.id)
        elif form.exgroup.data == -1 and form.isperkm.data == 1 and form.newgroup.data:
            cdtype = Cdtype(name=form.name.data, isperkm=True, group=form.newgroup.data, user_id=current_user.id)

        db.session.add(cdtype)
        db.session.commit()
        flash('New Cost Driver type successfully added', 'success')
        return redirect(url_for('cdtypes.overview'))

@cdtypes.route("/cdtype/overview" , methods=['GET', 'POST'])
@login_required
def overview():
    ps = Cdtype.query.filter_by(user_id=current_user.id).order_by()

    return render_template('cdtype_overview.html', cdtypelist=ps)





