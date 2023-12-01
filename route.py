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
        return home_pagina() 

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
        miRequest={}
        getRequest(miRequest)
        return ingresoUsuarioValido(miRequest)
     
    @app.route("/logout")
    def logout():  
        ''' Info: 
          Cierra la sesión.
          retorna la redirección a la pagina home   
        ''' 
        cerrarSesion()     
        return redirect('/')  

    @app.route("/editar_perfil")
    def edit_user():
        ''' Info:
          Carga la edit_user
          Retorna la edit_user, si hay sesion; sino retorna la home.
        '''
        param={}
        return editarPerfil_pagina(param)

    @app.route("/_editar_perfil")
    def edit():
        
        miRequest = {}
        getRequest(miRequest)
        return editarPerfil(miRequest)

    @app.route('/<name>')
    def noEncontrada(name):
        ''' Info:
          Entra en esta ruta todo direccionamiento recibido que 
          no machea con ningun otro route. Es decir no es un pagina (dirección)
            válida en el sistema.
          Retorna una pagina indicando el error. 
        '''  
        
        return paginaNoEncontrada(name)
    
    @app.route("/comisiones")
    def comisiones():
        
        param={}
        obtenerMensajeError(param)
        return comisiones_pantalla(param)
    
    @app.route("/agregar_comision", methods=["GET","POST"])
    def agregar_comision():
        
        miRequest={}
        getRequest(miRequest)
        return agregarComision(miRequest)

    @app.route("/materias")
    def materias():
        
        param={}
        obtenerMensajeError(param)
        return materias_pantalla(param)
    
    @app.route("/agregar_materia", methods=["GET","POST"])
    def agregar_materia():
        
        miRequest={}
        getRequest(miRequest)
        return agregarMateria(miRequest)

    @app.route("/cursos")
    def cursos():
        
        param={}
        obtenerMensajeError(param)
        return cursos_pantalla(param)
    
    @app.route("/agregar_curso", methods=["GET","POST"])
    def agregar_curso():
        
        miRequest={}
        getRequest(miRequest)
        return agregarCurso(miRequest)

    @app.route("/inscripciones")
    def inscripciones():
        param = {}
        obtenerMensajeError(param)
        return inscripciones_pantalla(param)
    
    @app.route("/agregar_inscripcion", methods=["GET","POST"])
    def agregar_inscripciones():
        miRequest={}
        getRequest(miRequest)
        return agregarInscripcion(miRequest)
    
    @app.route("/gestion_inscripciones")
    def gestion_inscripciones():
        param = {}
        obtenerMensajeError(param)
        return gestion_inscripciones_pantalla(param)

    @app.route('/inscribirse',methods = ["GET", "POST"])
    def inscribirse():
        miRequest={}
        getRequest(miRequest)
        return inscribirse(miRequest)






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
        return True#actualizarDatosDeUsuarios(param,request)  
    
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
     
    """ @app.route('/uploader', methods = ['GET', 'POST']) 
    def upload_file () : 

        if request.method == 'POST' :
            if 'file' not in request.files:
                flash('No file part')
            else:                
                f = request.files[ 'file' ]       
                #f = secure_filename(f.filename)
                
                #f.save( f.filename)
                f.savec
                return 'archivo cargado exitosamente' """
            
    # si existe el archivo devuelve True
    # os.path.exists(os.path.join('G:\\Mi unidad\\NUBE\\Docencia\\UCA\\_Materias\\03-UCA.PW\\_Python\\_PythonFlask\\07_login_register_bd\\uploadfile',"agua.png"))
    
    # borrar un archivo
    # os.remove(os.path.join('G:\\Mi unidad\\NUBE\\Docencia\\UCA\\_Materias\\03-UCA.PW\\_Python\\_PythonFlask\\07_login_register_bd\\uploadfile',"agua.png"))
    
    
    @app.route('/validate-username/<username>')
    def validate_username(username):
        try:
            # Conexión a la base de datos
            connection = mysql.connector.connect(**conectarBD)
            cursor = connection.cursor()

            # Consulta para verificar la existencia del usuario
            query = 'SELECT COUNT(*) FROM usuario WHERE usuario = %s'
            cursor.execute(query, (username,))
            count = cursor.fetchone()[0]

            # Cerrar la conexión
            cursor.close()
            connection.close()

            # Devolver la respuesta JSON
            return jsonify({'exists': count > 0})  #cantidad de registros (que coinciden) mayor a 0

        except Exception as e:
            return jsonify({'error': str(e)})
