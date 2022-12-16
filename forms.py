from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField  # fields to type  into input
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField("What's your name sir?", validators=[DataRequired()])
    submit = SubmitField("Submit")
