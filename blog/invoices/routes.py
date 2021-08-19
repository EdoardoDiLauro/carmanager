# coding=utf-8
import os

from flask import render_template, request, Blueprint, redirect, url_for, flash, abort, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from blog import db, ALLOWED_EXTENSIONS
from blog.models import Invoice, Car, Activity, CarCostProfile, Customer
from blog.invoices.forms import InvoiceForm
from datetime import datetime, time

invoices = Blueprint('invoices', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@invoices.route("/invoice/new", methods=['GET', 'POST'])
@login_required
def create_invoice():
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    form = InvoiceForm()

    if form.submit.data:
        if form.notes.data: invoice = Invoice( regdate=form.regdate.data , notes=form.notes.data ,user_id=current_user.id)
        else: invoice = Invoice( regdate=form.regdate.data, user_id=current_user.id)
        if form.doc.data and allowed_file(form.doc.data.filename):
            filename = secure_filename(str(form.causale.data) + '_' + str(form.data.data))
            form.doc.data.save(os.path.join(current_app.root_path, 'static/payment_files', filename))
            invoice.filename = filename

        db.session.add(invoice)
        db.session.commit()
        flash('New Invoice successfully added', 'success')
        return redirect(url_for('invoices.overview'))

    return render_template('create_invoice.html', title='New Invoice',
                           form=form, legend='New Invoice')

