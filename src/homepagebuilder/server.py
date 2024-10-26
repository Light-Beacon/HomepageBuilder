from Server.main import Server
from Core import config
config.fully_init()

s = Server()
app = s.get_flask_app()
