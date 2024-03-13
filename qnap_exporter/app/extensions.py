from flask_cors import CORS
from flask_apscheduler import APScheduler


scheduler = APScheduler()
cors = CORS  # not instantiated so we can use it in `__init__.py`
