import os
from flask import Flask, request, redirect, session, flash, url_for  
from controller import *

def route(app):

    @app.route("/")
    @app.route("/home")
    def home():
        ''' Info:
          Carga la pagina del home
        '''
        param={}
        return home_pagina(param) 
        
    
    @app.route("/login")
    def login():
        ''' Info:
          Carga la pagina del login
        ''' 
        param={}
        return login_pagina(param)

    @app.route("/register")
    def register():
        ''' Info:
          Carga la pagina para el registro del usuario
        '''
        param={}
        return register_pagina(param)
    
    @app.route("/cronograma")
    def cronograma():
        param={}
        return cronograma_pagina(param)
    
    @app.route("/inscripciones")
    def inscripciones():
        param={}
        obtenerMenuBottom(param)
        return render_template("GestionInscripciones.html", param=param)
    
    @app.route("/comisiones", methods=["GET","POST"])
    def comisiones():
        
        param={}
        miRequest={}
        getRequest(miRequest)
        return agregarComision(param, miRequest)
    
    @app.route("/materias", methods=["GET","POST"])
    def materias():
        
        param={}
        miRequest={}
        getRequest(miRequest)
        return agregarMateria(param, miRequest)
    
    @app.route("/perfil")
    def perfil():
        
        param={}
        return perfil_pagina(param)
        
    @app.route("/signup", methods =["GET", "POST"])
    def signup():
        ''' Info:
          Recepciona la solicitud request que es enviada
          desde el formulario de registro 
          registroDeUsuario: Luego de realizar el porceso de 
          registro del usuario, retorna la pagina del login 
        '''
        param={}
        miRequest={}
        getRequest(miRequest)
        return registrarUsuario(param,miRequest)

    @app.route('/signin', methods =["GET", "POST"])
    def signin(): 
        ''' Info:
          Recepciona la solicitud request que es enviada
          desde el formulario de login 
          retorna la pagina home en caso de exito 
                  o la pagina login en caso de fracaso
        '''
        param={}
        miRequest={}
        getRequest(miRequest)
        return ingresoUsuarioValido(param,miRequest)
     
    @app.route("/logout")
    def logout():  
        ''' Info: 
          Cierra la sesión.
          retorna la redirección a la pagina home   
        ''' 
        cerrarSesion()     
        return redirect('/')  


    @app.route("/edit_user")
    def edit_user():
        ''' Info:
          Carga la edit_user
          Retorna la edit_user, si hay sesion; sino retorna la home.
        '''
        param={}
        return editarUsuario_pagina(param)    
 

    @app.route("/update_user", methods =["GET", "POST"])
    def update_user():
        ''' Info:
          Recepciona la solicitud request que es enviada
              desde el formulario de edit_user 
          Retorna 
            si hay sesion: retorna la edit_user con los datos actualizados
               y un mensaje de exito o fracaso sobre el mismo form ; 
            si no hay sesion: retorna la home.
        '''
        param={}
        return actualizarDatosDeUsuarios(param,request)  

    @app.route('/recibir_datos',methods = ["GET", "POST"])
    def formrecibe():
        diRequest={}
        getRequest(diRequest)
        upload_file(diRequest)
        return  diRequest

    @app.route('/<name>')
    def noEncontrada(name):
        ''' Info:
          Entra en esta ruta todo direccionamiento recibido que 
          no machea con ningun otro route. Es decir no es un pagina (dirección)
            válida en el sistema.
          Retorna una pagina indicando el error. 
        '''  
        
        return paginaNoEncontrada(name)
    
    @app.route('/upload') 
    def  upload () : 
      return'''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="uploader" method="post" enctype="multipart/form-data">
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''
    
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
    @app.route('/uploader', methods = ['GET', 'POST']) 
    def upload_file () : 

        if request.method == 'POST' :
            if 'file' not in request.files:
                flash('No file part')
            else:                
                f = request.files[ 'file' ]       
                #f = secure_filename(f.filename)
                
                #f.save( f.filename)
                f.savec
                return 'archivo cargado exitosamente'
            
    # si existe el archivo devuelve True
    # os.path.exists(os.path.join('G:\\Mi unidad\\NUBE\\Docencia\\UCA\\_Materias\\03-UCA.PW\\_Python\\_PythonFlask\\07_login_register_bd\\uploadfile',"agua.png"))
    
    # borrar un archivo
    # os.remove(os.path.join('G:\\Mi unidad\\NUBE\\Docencia\\UCA\\_Materias\\03-UCA.PW\\_Python\\_PythonFlask\\07_login_register_bd\\uploadfile',"agua.png"))
    
    