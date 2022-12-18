from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField  # fields to type  into input
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField("What's your name sir?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField("Submit")
