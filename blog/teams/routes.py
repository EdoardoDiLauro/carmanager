# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Team, Car
from blog.teams.forms import TeamForm, AddCarForm
from datetime import datetime, time

teams = Blueprint('teams', __name__)

@teams.route("/team/new" , methods=['GET', 'POST'])
@login_required
def create_team():
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))
    form = TeamForm()
    if form.validate_on_submit():
        new_team = Team(name=form.name.data, user_id=current_user.id)
        db.session.add(new_team)
        db.session.commit()
        flash('New team successfully added', 'success')
        return redirect(url_for('teams.overview'))
    return render_template('create_team.html', title='Add Team', form=form, legend='Add Team')

@teams.route("/team/overview", methods=['GET', 'POST'])
@login_required
def overview():
    ps = Team.query.filter_by(user_id=current_user.id).order_by()

    return render_template('team_overview.html', teamlist=ps)


@teams.route("/team/<int:team_id>/delete", methods=['GET','POST'])
@login_required
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    if team.user_id != current_user.id:
        abort(403)
    db.session.delete(team)
    db.session.commit()
    flash('team successfully removed', 'success')
    return redirect(url_for('teams.overview'))

@teams.route("/team/<int:team_id>", methods=['GET','POST'])
@login_required
def team_detail(team_id):
    team = Team.query.get_or_404(team_id)
    if team.user_id != current_user.id:
        abort(403)

    form = TeamForm()


    carform = AddCarForm()
    cars = Car.query.filter(Car.user_id==current_user.id, Car.teams.any(id=team_id))
    carform.car.choices= [(-1," ")]+[(item.id, item.brand) for item in db.session.query(Car).filter(Car.user_id==current_user.id, ~Car.teams.any(id=team_id))]

    if form.validate_on_submit():
        team.name = form.name.data
        db.session.commit()
        flash('Team successfully updated', 'success')
        return redirect(url_for('teams.team_detail', team_id=team_id))
    elif request.method == 'GET':
        form.name.data = team.name
        form.submit.label.text = 'Update Team Name'

    if carform.validate_on_submit():
        if carform.car.data != -1:
            car = Car.query.get_or_404(carform.car.data)
            team.cars.append(car)
            db.session.commit()
            flash('Car successfully assigned', 'success')
        return redirect(url_for('teams.team_detail', team_id=team_id))

    return render_template('team.html', team=team, form=form, carform=carform, carlist=cars)

@teams.route("/team/<int:team_id>/remove/<int:car_id>", methods=['GET','POST'])
@login_required
def remove_car(team_id, car_id):
    team = Team.query.get_or_404(team_id)
    if team.user_id != current_user.id:
        abort(403)

    car = Car.query.get_or_404(car_id)

    car.teams.remove(team)
    db.session.commit()
    flash('Car successfully removed', 'success')
    return redirect(url_for('teams.team_detail', team_id=team_id))