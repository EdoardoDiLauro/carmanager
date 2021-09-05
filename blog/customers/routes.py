# coding=utf-8
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Event, Car, Activity, CarCostProfile, Customer
from blog.customers.forms import CustomerForm, UpdateCustomerForm, BindEventForm
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
        return redirect(url_for('customers.overview'))
    return render_template('create_customer.html', title='Add Customer', form=form, legend='Add Customer')

@customers.route("/customer/overview", methods=['GET', 'POST'])
@login_required
def overview():
    ps = Customer.query.filter_by(user_id=current_user.id).order_by()

    return render_template('customer_overview.html', customerlist=ps)

@customers.route("/customer/<int:customer_id>/delete", methods=['GET','POST'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.user_id != current_user.id:
        abort(403)

    evs = Event.query.filter_by(user_id=current_user.id, customer_id=customer_id)
    for ev in evs:
        ev.customer_id=0
        db.session.commit()

    db.session.delete(customer)
    db.session.commit()
    flash('Customer successfully removed', 'success')
    return redirect(url_for('customers.overview'))

@customers.route("/customer/<int:customer_id>", methods=['GET','POST'])
@login_required
def customer_detail(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.user_id != current_user.id:
        abort(403)

    evs = Event.query.filter_by(user_id=current_user.id, customer_id=customer_id)

    form = UpdateCustomerForm()
    bindform = BindEventForm()

    bindform.evs.choices = [(-1, " ")] + [(item.id, item.name) for item in
                                      db.session.query(Event).filter(
                                          Event.user_id == current_user.id).filter(
                                          Event.customer_id == 0)]

    if bindform.validate_on_submit() and bindform.evs.data != -1:
        ev =  Event.query.get_or_404(bindform.evs.data)
        ev.customer_id =customer_id
        db.session.commit()

    if form.validate_on_submit():
        customer.name = form.name.data
        customer.address = form.address.data
        customer.notes = form.notes.data
    elif request.method == "GET":
        form.name.data = customer.name
        form.address.data = customer.address
        form.notes.data=customer.notes
    return render_template('customer.html', title='Update Customer', bindform=bindform,form=form, eventlist=evs, customer=customer, legend='Update Customer')

@customers.route("/customer/<int:customer_id>/<int:event_id>/unbind", methods=['GET','POST'])
@login_required
def unbind_event(customer_id,event_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.user_id != current_user.id:
        abort(403)

    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    event.customer_id = 0
    db.session.commit()
    flash('Customer successfully removed from event', 'success')
    return redirect(url_for('customers.customer_detail', customer_id=customer_id))