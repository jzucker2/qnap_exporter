from flask_cors import CORS
from flask_migrate import Migrate
from flask_apscheduler import APScheduler


scheduler = APScheduler()
migrate = Migrate()
cors = CORS  # not instantiated so we can use it in `__init__.py`
