import os
from flask import Flask, session
from route import route

def main():
    app = Flask(__name__,template_folder='templates',static_folder='static')
    
    # C O N F I G
    # Para poder iniciar session, colocar un string aleatorio para inicializar la clave.
    app.config['SECRET_KEY'] = 'some random string'  


    route(app)
    app.run('0.0.0.0', 5000, debug=True) 
    
main()