# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Event, Car, Activity, CarCostProfile, Customer
from blog.customers.forms import CustomerForm
from datetime import datetime, time

customers = Blueprint('customers', __name__)

@customers.route("/customer/new" , methods=['GET', 'POST'])
@login_required
def create_customer():
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    form = CustomerForm()

    if form.validate_on_submit():
        if form.notes.data : new_customer = Customer(name=form.name.data, address=form.address.data, notes=form.notes.data, user_id=current_user.id)
        else:new_customer = Customer(name=form.name.data, address=form.address.data, user_id=current_user.id)
        db.session.add(new_customer)
        db.session.commit()
        flash('New Customer successfully added', 'success')
        return redirect(url_for('events.overview'))
    return render_template('create_customer.html', title='Add Customer', form=form, legend='Add Customer')