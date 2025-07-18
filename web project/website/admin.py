from flask import Blueprint, render_template,  request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from .models import AssetRequest, ExpenseRequest, DailyLogs
from . import db
from website.utils import get_branches_from_excel, get_assets_from_csv

admin = Blueprint('admin', __name__)


@admin.route('/admin')
def admin_products():
    return render_template('admin.html')

@admin.route('/admin/expenses')
def expenses():
    requests = ExpenseRequest.query.order_by(ExpenseRequest.date_submitted.desc()).all()
    return render_template('admin_expenses.html',requests=requests)

@admin.route('/admin/product-requests')
def product():
    requests = AssetRequest.query.order_by(AssetRequest.date_requested.desc()).all()
    return render_template('admin_product.html', requests=requests)

@admin.route('/admin/support')
def support():
    return render_template('admin_support.html')

@admin.route('/admin/assets')
def assets():
    return render_template('admin_assets.html')

@admin.route('/admin/logs')
def logs():
    requests = DailyLogs.query.order_by(DailyLogs.date_submitted.desc()).all()
    return render_template('admin_logs.html', requests=requests)