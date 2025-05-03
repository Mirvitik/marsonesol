from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    id = StringField('Id астронавта', validators=[DataRequired()])
    password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    captain_id = StringField('Id капитана', validators=[DataRequired()])
    captain_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')


class JobForm(FlaskForm):
    work = StringField('Job Title', validators=[DataRequired()])
    id = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Заголовок', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField("Is job hinished?")
    submit = SubmitField('Применить')
