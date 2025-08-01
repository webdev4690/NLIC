from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('views.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Invalid username', 'danger')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password_hash, password):
            flash('Incorrect password', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash(f"Welcome, {user.username}! You have successfully logged in.", "success")

        if user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))  
            '''elif user.role == 'gs':
            return redirect(url_for('gs.gs_dashboard'))'''     
        else:
            return redirect(url_for('views.home'))   

    return render_template('login.html')


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user() 
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))