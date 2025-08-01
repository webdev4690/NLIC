from flask import Blueprint, render_template,  request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from .models import AssetRequest, ExpenseRequest, DailyLogs
from . import db
from website.utils import get_branches_from_excel, get_assets_from_csv, get_issue_from_excel, role_required
from flask_login import login_required

UPLOAD_FOLDER = 'static/uploads/'
views = Blueprint('views', __name__)

@views.route('/home')
@login_required
@role_required('user', 'admin')
def home():
    return render_template('home.html')

@views.route('/Expenses', methods=['GET', 'POST'])
@login_required
@role_required('user', 'admin')
def expenses():
    branches = get_branches_from_excel()
    assets = get_assets_from_csv()
    if request.method == 'POST':
        branch = request.form.get('branch')
        item = request.form.get('item')
        description = request.form.get('description')
        amount = request.form.get('amount')
        expense_month = request.form.get('expense_month')
        approver = request.form.get('approver')

        file = request.files.get('letter')
        filename = None
        if file and file.filename != '':
            filename = file.filename
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
    
        new_expense = ExpenseRequest(
            branch=branch,
            item=item,
            description=description,
            amount=float(amount) if amount else None,
            expense_month=expense_month if expense_month else None,
            approver=approver,
            letter_filename=filename
        )

        db.session.add(new_expense)
        db.session.commit()

        flash('✅ Expense request submitted successfully!', 'success')
        return redirect(url_for('views.expenses'))
    
    return render_template('expenses.html', branches=branches, assets=assets)

@views.route('/New_Product', methods=['GET', 'POST'])
@login_required
@role_required('user', 'admin')
def product():
    branches = get_branches_from_excel()
    if request.method == 'POST':
        branch = request.form.get('branch')
        asset_name = request.form.get('asset_name')
        description = request.form.get('description')
        amount = request.form.get('amount')
        approver = request.form.get('approver')
        old_condition = request.form.get('old_condition')
        old_location = request.form.get('old_location')
        old_code = request.form.get('old_code')
        quantity = request.form.get('quantity')

        file = request.files.get('attachment')
        filename = None
        if file and file.filename != '':
            filename = file.filename
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True) 
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

        new_request = AssetRequest(
            branch=branch,
            asset_name=asset_name,
            description=description,
            amount=float(amount) if amount else None,
            approver=approver,
            old_condition=old_condition,
            old_location=old_location,
            old_code=old_code if old_code else None,
            quantity=int(quantity),
            attachment=filename
        )

        db.session.add(new_request)
        db.session.commit()

        flash('✅ Asset request submitted successfully!', 'success')
        return redirect(url_for('views.product'))

    return render_template('new_product.html', branches=branches)

@views.route('/Assets')
@login_required
@role_required('user', 'admin')
def assets():
    return render_template('assets.html')

@views.route('/Logs', methods=['GET', 'POST'])
@login_required
@role_required('user', 'admin')
def logs():
    branches = get_branches_from_excel()
    issues = get_issue_from_excel()

    if request.method == 'POST':
        branch = request.form.get('branch')
        issue_type = request.form.get('issue_type')
        issue_description = request.form.get('issue_description')
        asset_code = request.form.get('assets_code')
        communication_channel = request.form.get('communication_channel')
        issue_generated_by = request.form.get('generated_by')
        replaced_description = request.form.get('replaced_part_description')
        replaced_cost = request.form.get('replaced_cost')
        status = request.form.get('status')
        support_station = request.form.get('support_station')
        remarks = request.form.get('remarks')

        new_log = DailyLogs(
            branch=branch,
            issue_type=issue_type,
            issue_description=issue_description,
            asset_code=asset_code,
            communication_channel=communication_channel,
            issue_generated_by=issue_generated_by,
            replaced_description=replaced_description,
            replaced_cost=float(replaced_cost) if replaced_cost else None,
            status=status,
            support_station=support_station,
            remarks=remarks
        )

        db.session.add(new_log)
        db.session.commit()

        flash('✅ Daily log submitted successfully!', 'success')
        return redirect(url_for('views.logs'))
    return render_template('logs.html', branches=branches, issues=issues)

