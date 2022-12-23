from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField  # fields to type  into input
from wtforms.validators import DataRequired, EqualTo, Length


class NameForm(FlaskForm):
    name = StringField("What's your name sir?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField("Submit")
    school_study = StringField('School Study')
    password_hash = PasswordField('Password',
                                  validators=[DataRequired(),
                                              EqualTo('password_hash2',
                                                      message='Password must much')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])


class PasswordForm(FlaskForm):
    email = StringField("What's your name sir?", validators=[DataRequired()])
    password_hash = PasswordField("What's your password sir?", validators=[DataRequired()])
    submit = SubmitField("Submit")

