from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import model_load
model, lb, le = model_load.get_modeldata()

from app import routes, models, errors


from app import preprocessDB_Codechef as ppcc
ppcc.run()

from app import preprocessDB_Codeforces as ppcf
ppcf.run()



