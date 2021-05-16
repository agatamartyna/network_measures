import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
   SECRET_KEY = os.environ.get("SECRET_KEY") or "remember-to-add-secret-key"
   ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
   ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
