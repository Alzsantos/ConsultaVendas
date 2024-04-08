from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile('config.py')
csrf = CSRFProtect(app)

from views_consulta import *

if __name__=='__main__':
    with app.app_context():
        app.run()
    



