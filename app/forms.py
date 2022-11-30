from flask_login import current_user
from flask_wtf import FlaskForm
import wtforms as ws



class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[
        ws.validators.DataRequired(), ws.validators.Length(min=4, max=20)])
    password = ws.PasswordField('Пароль', validators=[
        ws.validators.DataRequired(), ws.validators.Length(min=8, max=24)])



class TransactionsForm(FlaskForm):
    period = ws.StringField('Период транзакции')
    value = ws.IntegerField('Сумма')
    status = ws.StringField('Статус')
    unit = ws.StringField('Валюта')
    subject = ws.StringField('Комментарии')
    admin_name = current_user
