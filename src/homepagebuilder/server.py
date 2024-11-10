from server.main import Server
from core import config
config.fully_init()

s = Server()
app = s.get_flask_app()
