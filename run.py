import os
from flask import Flask
from route import route


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # C O N F I G
    # La clave de sesión se toma de la variable de entorno SECRET_KEY en
    # produccion; en local cae al valor por defecto.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'some random string')

    route(app)
    return app


# Instancia WSGI que usan tanto el servidor local como Vercel (api/index.py).
app = create_app()


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
