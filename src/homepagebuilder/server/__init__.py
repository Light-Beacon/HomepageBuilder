from .main import Server
def app():
    import os
    server = Server(os.getcwd() + os.path.sep + 'Project.yml')
    return server.get_flask_app()
