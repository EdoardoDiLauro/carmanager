# coding=utf-8
import os

from flask import render_template, request, Blueprint, redirect, url_for, flash, abort, current_app, \
    send_from_directory, send_file, Response
from flask_login import current_user, login_required
from io import BytesIO
from werkzeug.wsgi import FileWrapper
from blog import db, ALLOWED_EXTENSIONS
from blog.models import Invoice, Car, Activity, CarCostProfile, Customer, Spare
from blog.invoices.forms import InvoiceForm, UpdateInvoiceForm
from blog.spares.forms import SpareFormDash, SpareDashForm
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
        if form.notes.data: invoice = Invoice( regdate=form.regdate.data , supplier=form.supplier.data,notes=form.notes.data ,user_id=current_user.id)
        else: invoice = Invoice( regdate=form.regdate.data, user_id=current_user.id)
        if form.doc.data and allowed_file(form.doc.data.filename):
            extension = form.doc.data.filename.rsplit('.', 1)[1].lower()
            filename = str(form.supplier.data) +'_'+ str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))+'_'+ str(current_user.id)+ '.' + extension
            invoice.filename = filename
            form.doc.data.save(os.path.join(current_app.root_path, 'static\payment_files', filename))

        db.session.add(invoice)
        db.session.commit()
        flash('New Invoice successfully added', 'success')
        return redirect(url_for('invoices.overview'))

    return render_template('create_invoice.html', title='New Invoice',
                           form=form, legend='New Invoice')

@invoices.route("/invoice/overview" , methods=['GET', 'POST'])
@login_required
def overview():
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    ps = Invoice.query.filter_by(user_id=current_user.id).order_by()

    return render_template('invoice_overview.html', invoicelist=ps)

@invoices.route('/invoice/files/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static/payment_files'), filename)

@invoices.route('/invoice/files/dl/<filename>')
@login_required
def download_file(filename):
    f = open(os.path.join(current_app.root_path, 'static/payment_files', filename), "rb")
    b = BytesIO(f.read())
    file_wrapper = FileWrapper(b)
    headers = {
        'Content-Disposition': 'attachment; filename="{}"'.format(filename)
    }
    response = Response(file_wrapper,
                        mimetype='application/pdf',
                        headers=headers)
    return response
@invoices.route("/invoice/<int:invoice_id>/detail", methods=['GET', 'POST'])
@login_required
def invoice_detail(invoice_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    invoice = Invoice.query.get_or_404(invoice_id)
    if invoice.user_id != current_user.id:
        abort(403)

    form = UpdateInvoiceForm()
    availdashform = SpareDashForm()
    useddashform = SpareDashForm()

    usedspares = db.session.query(Spare).filter(
        Spare.invoice_id == invoice_id, Spare.user_id == current_user.id)

    availablespares = db.session.query(Spare).filter(
        Spare.invoice_id == 0, Spare.user_id == current_user.id)
    
    for sp in availablespares:
        sp_form = SpareFormDash()
        sp_form.spid = sp.id
        sp_form.nome =sp.name
        sp_form.isnew = sp.isnew
        sp_form.price = sp.price
        sp_form.notes = sp.notes
        availdashform.sps.append_entry(sp_form)

    invoice.totprice = 0

    for sp in usedspares:
        sp_form = SpareFormDash()
        sp_form.spid = sp.id
        sp_form.nome =sp.name
        sp_form.isnew = sp.isnew
        sp_form.price = sp.price
        sp_form.notes = sp.notes
        invoice.totprice = invoice.totprice + sp.price
        db.session.commit()
        useddashform.sps.append_entry(sp_form)

    if availdashform.submit.data:
        for data in availdashform.sps.entries:
            if data.select.data == 1:
                spmod = Spare.query.filter_by(id=data.spid.data).first()
                spmod.invoice_id = invoice_id
                db.session.commit()
        flash('Spare Parts successfully assigned', 'success')
        return redirect(url_for('invoices.invoice_detail', invoice_id=invoice_id))

    if useddashform.submitoff.data:
        for data in useddashform.sps.entries:
            if data.select.data == 1:
                spmod = Spare.query.filter_by(id=data.spid.data).first()
                spmod.invoice_id = 0
                db.session.commit()
        flash('Spare Parts successfully discarded', 'success')
        return redirect(url_for('invoices.invoice_detail', invoice_id=invoice_id))


    if form.validate() and form.supplier.data and form.regdate.data:
        invoice.supplier = form.supplier.data
        invoice.regdate = form.regdate.data
        db.session.commit()
        flash('Invoice successfully updated', 'success')
        return redirect(url_for('invoices.detail', invoice_id=invoice_id))
    if form.validate() and form.supplier.data and form.regdate.data and form.notes.data:
        invoice.supplier = form.supplier.data
        invoice.notes = form.notes.data
        db.session.commit()
        flash('Invoice successfully updated', 'success')
        return redirect(url_for('invoices.detail', invoice_id=invoice_id))
    elif request.method == 'GET':
        form.supplier.data = invoice.supplier
        form.regdate.data = invoice.regdate
        form.notes.data = invoice.notes

    return render_template('invoice_detail.html', invoice=invoice,availspares=availdashform, usedspares=useddashform, title='Invoice Detail',
                           form=form, legend='Update Invoice')

@invoices.route("/invoice/<int:invoice_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_invoice(invoice_id):
    if not current_user.is_authenticated:
        flash('Please log in to access current page', 'danger')
        return redirect(url_for('main.home'))

    invoice = Invoice.query.get_or_404(invoice_id)
    if invoice.user_id != current_user.id:
        abort(403)

    usedspares = db.session.query(Spare).filter(
        Spare.invoice_id == invoice_id, Spare.user_id == current_user.id)

    for sp in usedspares:
        sp.invoice_id = 0

    db.session.delete(invoice)
    db.session.commit()
    flash('Invoice successfully removed', 'success')
    return redirect(url_for('invoices.overview'))