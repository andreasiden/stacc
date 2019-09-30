from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_table import Table, Col
from mainapp import *


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

