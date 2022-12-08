from flask import Flask, render_template

from main.views import main
from loader.views import loader

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.register_blueprint(main)
app.register_blueprint(loader)


@app.errorhandler(404)
def not_uploaded(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
