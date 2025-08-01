from flask import Blueprint, render_template,  request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from .models import AssetRequest, ExpenseRequest, DailyLogs
from . import db
from website.utils import get_branches_from_excel, get_assets_from_csv, role_required
from flask_login import login_required

admin = Blueprint('admin', __name__)
approver_names = {
        "gokul.jha@nepallife.com.np": "Gokul Jha",
        "suraj.chapagain@nepallife.com.np": "Suraj Chapagain"
    }

@admin.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    return render_template('admin.html')

@admin.route('/admin/expenses')
@login_required
@role_required('admin')
def expenses():
    expenses = ExpenseRequest.query.order_by(ExpenseRequest.date_submitted.desc()).all()
    return render_template('admin_expenses.html',expenses=expenses)

@admin.route('/admin/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_expense(expense_id):
    expense = ExpenseRequest.query.get_or_404(expense_id)
    assets = get_assets_from_csv()
    if request.method == 'POST':
        expense.item = request.form['item']
        expense.description = request.form['description']
        expense.amount = float(request.form['amount'])
        expense.expense_month = request.form['expense_month']
        expense.approver = request.form['approver']

        db.session.commit()
        flash('Expense updated successfully.', 'success')
        return redirect(url_for('admin.expenses'))

    return render_template('edit_expense.html', expense=expense, assets=assets, approver_names=approver_names)

@admin.route('/admin/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_expense(expense_id):
    expense = ExpenseRequest.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash(f'Expense ID {expense_id} has been deleted.', 'warning')
    return redirect(url_for('admin.expenses'))

@admin.route('/admin/product-requests')
@login_required
@role_required('admin')
def product():
    requests = AssetRequest.query.order_by(AssetRequest.date_requested.desc()).all()
    return render_template('admin_product.html', requests=requests)

@admin.route('/admin/product-requests/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_product(product_id):
    product = AssetRequest.query.get_or_404(product_id)
    if request.method == 'POST':
        product.asset_name = request.form['asset_name']
        product.description = request.form['description']
        product.amount = float(request.form['amount'])
        product.approver = request.form['approver']
        product.old_condition = request.form['old_condition']
        product.old_location = request.form['old_location']
        product.old_code = request.form['old_code']
        product.quantity = request.form['quantity']

        db.session.commit()
        flash('Expense updated successfully.', 'success')
        return redirect(url_for('admin.product'))

    return render_template('edit_product.html', product=product,approver_names=approver_names)

@admin.route('/admin/product-requests/delete/<int:product_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_product(product_id):
    expense = AssetRequest.query.get_or_404(product_id)
    db.session.delete(expense)
    db.session.commit()
    flash(f'Expense ID {product_id} has been deleted.', 'warning')
    return redirect(url_for('admin.product'))


@admin.route('/admin/support')
@login_required
@role_required('admin')
def support():
    return render_template('admin_support.html')

@admin.route('/admin/assets')
@login_required
@role_required('admin')
def assets():
    return render_template('admin_assets.html')

@admin.route('/admin/logs')
@login_required
@role_required('admin')
def logs():
    requests = DailyLogs.query.order_by(DailyLogs.date_submitted.desc()).all()
    return render_template('admin_logs.html', requests=requests)