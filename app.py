from flask import Flask, render_template, flash
from forms import NameForm, UserForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

app.config['SECRET_KEY'] = "my secret key to world"

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create string

    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/')
def home():  # put application's code here
    return render_template('home.html')


@app.route('/user/<name>/')
def user(name):  # put application's code here
    return render_template('user.html', name=name)


@app.errorhandler(404)
def custom_err(err):
    return render_template('error404.html'), 404


@app.errorhandler(500)
def internal_server_error(err):
    return render_template('error505.html'), 500


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted successfully")

    return render_template('name.html',
                           name=name,
                           form=form)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
