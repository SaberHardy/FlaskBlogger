from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField  # fields to type  into input
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea


class NameForm(FlaskForm):
    name = StringField("What's your name sir?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('User name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    profile_picture = FileField("Profile Picture")
    submit = SubmitField("Update user")
    school_study = StringField('School Study')
    about_author = TextAreaField('About The author')
    password_hash = PasswordField('Password',
                                  validators=[DataRequired(),
                                              EqualTo('password_hash2',
                                                      message='Password must much')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])


class PasswordForm(FlaskForm):
    email = StringField("What's your name sir?", validators=[DataRequired()])
    password_hash = PasswordField("What's your password sir?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Content', validators=[DataRequired()])
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login user")


class SearchForm(FlaskForm):
    searched = StringField("What are you searching for", validators=[DataRequired()])
    submit = SubmitField("Search")
