from app import app
from .routes.api import api
from .routes.root import root

app.register_blueprint(root, url_prefix="/")
app.register_blueprint(api, url_prefix="/api")


