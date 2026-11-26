import os
from pathlib import Path
from secrets import token_urlsafe

SECRET_KEY = token_urlsafe(48)
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ROOT_URLCONF = "urls"
INSTALLED_APPS = ["ledger"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("REPORT_DB", str(Path(__file__).with_name("report.sqlite3"))),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
