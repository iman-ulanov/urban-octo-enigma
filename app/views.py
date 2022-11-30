from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user

from app import db
from .forms import TransactionsForm, UserForm
from .models import Transactions, User


def all_transactions():
    transactions = Transactions.query.all()
    return render_template('transactions_view.html', transactions=transactions)


@login_required
def transactions_add():
    form = TransactionsForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            transaction = Transactions()
            form.populate_obj(transaction)
            db.session.add(transaction)
            db.session.commit()
            flash('Транзакция сохранена!', 'success')
            return redirect(url_for('transactions_view'))
    return render_template('transaction_form.html', form=form)


def transactions_detail(id):
    transactions = Transactions.query.get(id)
    return render_template('transactions_detail.html', transactions=transactions)


@login_required
def transactions_update(id):
    transaction = Transactions.query.get(id)
    form = TransactionsForm(request.form, obj=transaction)
    if transaction.admin_name != current_user.username:
        return('У вас нет доступа!')
    if transaction.admin_name != current_user.username:
        abort(403)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(transaction)
            db.session.add(transaction)
            db.session.commit()
            flash('Транзакция сохранена!', 'info')
            return redirect(url_for('transactions_view'))
    return render_template('transaction_form.html', form=form)


@login_required
def transactions_delete(id):
    transaction = Transactions.query.get(id)
    if transaction.admin_name != current_user.username:
        return 'У вас нет доступа!'
    if transaction.admin_name != current_user.username:
        abort(403)
    if request.method == 'POST':
        db.session.delete(transaction)
        db.session.commit()
        flash('Транзакция сохранена!', 'warning')
        return redirect(url_for('transactions_view'))
    return render_template('transaction_delete.html', transaction=transaction)


def register_view():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            flash(f'Пользователь {user.username} успешно зарегистрирован!', 'success')
            return redirect(url_for('login'))
    return render_template('user_form.html', form=form)


def login_view():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            #     user = User()
            #     form.populate_obj(user)
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('Успешно авторизован!', 'primary')
                return redirect(url_for('transactions_view'))
            else:
                flash('Неправильно введенные логин или пароль', 'danger')
    return render_template('login.html', form=form)


def logout_view():
    logout_user()
    return redirect(url_for('login'))
