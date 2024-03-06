from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateTimeField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Работа', validators=[DataRequired()])
    work_size = IntegerField("Содержание")
    collaborators = StringField("Соучастники")
    start_date = DateTimeField("Дата начало", format="%d/%m/%Y")
    end_date = DateTimeField("Дата окончание", format="%d/%m/%Y")
    is_finished = BooleanField("Законченная работа")
    team_leader = IntegerField("Капитан")
    submit = SubmitField('Применить')