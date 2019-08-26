from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    """Returns homepage."""
    return render_template('home.html', msg='Flask is cool, and working.')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
