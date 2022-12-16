from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
