from flask import Flask
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('flask_ventas.config.Config')

mysql = MySQL(app)
Bootstrap(app)

from flask_ventas import routes

if __name__ == "__main__":
    app.run(debug=True)
