from flask import Flask, render_template, flash, request, redirect, url_for
from forms import NameForm, UserForm, PasswordForm, PostForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Add database
# Old database
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
# new db
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/users"

app.config['SECRET_KEY'] = "my secret key to world"

db = SQLAlchemy(app)

# Migrate the app with database
migrate = Migrate(app, db)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    school_study = db.Column(db.String(300))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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


@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        form.email.data = ''
        form.password_hash.data = ''

        # flash("Form Submitted successfully")
        # If the information input were written
        pw_to_check = Users.query.filter_by(email=email).first()
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template('test_pw.html',
                           email=email,
                           password=password,
                           pw_to_check=pw_to_check,
                           passed=passed,
                           form=form)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data,
                         email=form.email.data,
                         school_study=form.school_study.data,
                         password_hash=hashed_pw
                         )
            db.session.add(user)
            db.session.commit()

        name = form.name.data

        form.name.data = ""
        form.email.data = ""
        form.school_study.data = ""
        form.password_hash.data = ""

        flash("User added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)


@app.route('/update/<int:id>/', methods=['POSt', 'GET'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.school_study = request.form['school_study']
        try:
            db.session.commit()
            flash('User updated successfully!!')
            return redirect(url_for('add_user'))
        except:
            flash('The update can\'t be completed')
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template('update.html',
                               form=form,
                               name_to_update=name_to_update,
                               id=id)


@app.route('/delete/<int:id>/', methods=['POST', 'GET'])
def delete(id):
    name = None
    form = UserForm()
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User was deleted successfully")
        flash("User added successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html',
                               form=form,
                               name=name,
                               our_users=our_users)
    except:
        flash("We cant find your user to delete")
        return render_template('add_user.html',
                               form=form,
                               name=name,
                               our_users=our_users)


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data,
                     content=form.content.data,
                     author=form.author.data,
                     slug=form.slug.data)

        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add the post to the database
        db.session.add(post)
        db.session.commit()

        flash("Your post added successfully")

    return render_template('blog/add_post.html', form=form)


@app.route('/retrieve', methods=['POST', 'GET'])
def retrieve_all_posts():
    posts = Posts.query.order_by(-Posts.date_posted).all()  # Order by last added
    return render_template('blog/all_posts.html', posts=posts)


@app.route('/detail/<int:id>/', methods=['POST', 'GET'])
def post_detail(id):
    get_post = Posts.query.get_or_404(id)

    return render_template('blog/post_detail.html', get_post=get_post)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
