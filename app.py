from flask import Flask, render_template, flash, request, redirect, url_for
from forms import NameForm, UserForm, PasswordForm, PostForm, LoginForm, SearchForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(
            username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,
                                   form.password.data):
                login_user(user)
                flash("Login successfully!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password, try again!!!!!!!")
        else:
            flash("The user doesnt exist!!")

    return render_template('members/login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()

    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.school_study = request.form['school_study']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash('User updated successfully!!')
            return render_template('members/dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update
                                   )
        except:
            flash('The update can\'t be completed')
            return render_template('members/dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template('members/dashboard.html',
                               form=form,
                               name_to_update=name_to_update,
                               id=id)
    # return render_template('members/dashboard.html')


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    school_study = db.Column(db.String(300))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Posts', backref='poster')

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


# @app.route('/')
# def home():  # put application's code here
#     return render_template('home.html')


@app.route('/user/<name>/')
def user(name):  # put application's code here
    return render_template('users/user.html', name=name)


@app.errorhandler(404)
def custom_err(err):
    return render_template('users/error404.html'), 404


@app.errorhandler(500)
def internal_server_error(err):
    return render_template('users/error505.html'), 500


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted successfully")

    return render_template('users/name.html',
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

    return render_template('users/test_pw.html',
                           email=email,
                           password=password,
                           pw_to_check=pw_to_check,
                           passed=passed,
                           form=form)


@app.route('/user/add', methods=['GET', 'POST'])
# @login_required
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                school_study=form.school_study.data,
                password_hash=hashed_pw
            )
            db.session.add(user)
            db.session.commit()

        form.name.data = ""
        form.username.data = ""
        form.email.data = ""
        form.school_study.data = ""
        form.password_hash.data = ""

        flash("User added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('users/add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)


@app.route('/delete_user/<int:id>/')
@login_required
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("users/add_user.html",
                               form=form,
                               name=name,
                               our_users=our_users)

    except:
        flash("Whoops! There was a problem deleting user, try again...")
        return render_template("users/add_user.html",
                               form=form, name=name, our_users=our_users)


@app.route('/update/<int:id>/', methods=['POSt', 'GET'])
# @login_required
def update_user_profile(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.school_study = request.form['school_study']
        name_to_update.name = request.form['name']
        try:
            db.session.commit()
            flash('User updated successfully!!')
            return redirect(url_for('add_user'))
        except:
            flash('The update can\'t be completed')
            return render_template('users/update.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
    else:
        return render_template('users/update.html',
                               form=form,
                               name_to_update=name_to_update,
                               id=id)


@app.route('/delete/<int:id>/')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    if current_user.id == post_to_delete.poster.id:

        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            # Return a message
            flash("Blog Post Was Deleted!")

            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("blog/all_posts.html", posts=posts)

        except:
            # Return an error message
            flash("Whoops! There was a problem deleting post, try again...")

            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("blog/all_posts.html", posts=posts)
    else:
        flash("You are not authorized to delete this post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("blog/all_posts.html", posts=posts)


@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    flag = 'Create'
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data,
                     content=form.content.data,
                     # author=form.author.data,
                     slug=form.slug.data,
                     poster_id=poster
                     )

        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add the post to the database
        db.session.add(post)
        db.session.commit()

        flash("Your post added successfully")

    return render_template('blog/add_post.html', form=form, flag=flag)


@app.route('/', methods=['POST', 'GET'])
def retrieve_all_posts():
    posts = Posts.query.order_by(-Posts.date_posted).all()  # Order by last added
    return render_template('blog/all_posts.html', posts=posts)


@app.route('/detail/<int:id>/', methods=['POST', 'GET'])
def post_detail(id):
    get_post = Posts.query.get_or_404(id)

    return render_template('blog/post_detail.html', get_post=get_post)


@app.route('/edit/<int:id>/', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    flag = 'Edit'
    post_edit = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post_edit.title = form.title.data
        post_edit.content = form.content.data
        # post_edit.author = form.author.data
        post_edit.slug = form.slug.data

        db.session.add(post_edit)
        db.session.commit()

        flash("Post has been updated successfully!")
        return redirect(url_for('retrieve_all_posts', id=post_edit.id))

    form.title.data = post_edit.title
    form.content.data = post_edit.content
    # form.author.data = post_edit.author
    form.slug.data = post_edit.slug

    return render_template('blog/add_post.html', form=form, flag=flag)


@app.route('/update-profile/<int:id>/', methods=['POST', 'GET'])
@login_required
def edit_profile(id):
    pass


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# Create Search Function
@app.route('/search', methods=["POST"])
@login_required
def search_post():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from submitted form
        post_searched = form.searched.data
        # Query the Database
        posts = posts.filter(Posts.content.like('%' + post_searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template("blog/searched.html",
                               form=form,
                               searched=post_searched,
                               posts=posts)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
