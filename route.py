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
        obtenerMensajes(param)
        return login_pagina(param)

    @app.route("/register")
    def register():
        ''' Info:
          Carga la pagina para el registro del usuario
        '''
        param={}
        obtenerMensajes(param)
        return register_pagina(param)
    
    @app.route("/cronograma")
    def cronograma():
        param={}
        param["inscripcion"] = ""
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
        obtenerMensajes(param)
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
        obtenerMensajes(param)
        return comisiones_pantalla(param)
    
    @app.route("/agregar_comision", methods=["GET","POST"])
    def agregar_comision():
        
        miRequest={}
        getRequest(miRequest)
        return agregarComision(miRequest)

    @app.route("/materias")
    def materias():
        
        param={}
        obtenerMensajes(param)
        return materias_pantalla(param)
    
    @app.route("/agregar_materia", methods=["GET","POST"])
    def agregar_materia():
        
        miRequest={}
        getRequest(miRequest)
        return agregarMateria(miRequest)

    @app.route("/cursos")
    def cursos():
        
        param={}
        obtenerMensajes(param)
        return cursos_pantalla(param)
    
    @app.route("/agregar_curso", methods=["GET","POST"])
    def agregar_curso():
        
        miRequest={}
        getRequest(miRequest)
        return agregarCurso(miRequest)

    @app.route("/inscripciones")
    def inscripciones():
        param = {}
        obtenerMensajes(param)
        return inscripciones_pantalla(param)
    
    @app.route("/agregar_inscripcion", methods=["GET","POST"])
    def agregar_inscripciones():
        miRequest={}
        getRequest(miRequest)
        return agregarInscripcion(miRequest)
    
    @app.route("/gestion_inscripciones")
    def gestion_inscripciones():
        param = {}
        obtenerMensajes(param)
        return gestion_inscripciones_pantalla(param)

    @app.route('/inscribirse',methods = ["GET", "POST"])
    def inscribirse():
        miRequest={}
        getRequest(miRequest)
        return inscripcion_usuario(miRequest)
       




    
    # @app.route('/validate-username/<username>')
    # def validate_username(username):
    #     try:
    #         # Conexión a la base de datos
    #         connection = mysql.connector.connect(**conectarBD)
    #         cursor = connection.cursor()

    #         # Consulta para verificar la existencia del usuario
    #         query = 'SELECT COUNT(*) FROM usuario WHERE usuario = %s'
    #         cursor.execute(query, (username,))
    #         count = cursor.fetchone()[0]

    #         # Cerrar la conexión
    #         cursor.close()
    #         connection.close()

    #         # Devolver la respuesta JSON
    #         return jsonify({'exists': count > 0})  #cantidad de registros (que coinciden) mayor a 0

    #     except Exception as e:
    #         return jsonify({'error': str(e)})

    # def verificarUsuario():
    #       form_data = request.form
    #       return verUsuario()

    @app.route('/validar_usuario/<username>', methods=['POST','GET'])
    def verificarUsuario(username):
        try:
            if username:
                respuesta_verificacion = verUsuario(username)
                return respuesta_verificacion
            else:
             return 'El nombre de usuario no puede estar vacío.'
        except Exception as e:
            print(f"Error en la ruta /validar_usuario: {str(e)}")
            return 'Error interno del servidor', 500

    @app.route('/validar_email/<email>', methods=['POST','GET'])
    def verificarEmail(email):
        try:
            if email:
                res = verEmail(email)
                return res
            else:
                return 'El email no puede estar vacío.'
        except Exception as e:
            print(f"Error en la ruta /validar_email: {str(e)}")
            return 'Error interno del servidor', 500

    @app.route('/validar_estado/<option>', methods=['POST', 'GET'])
    def verificarOpcion(option):
        try:
            option = request.form.get('estado', '').strip()
            if option:
                if option=="abierta":    
                    resVerificacion = verEstado(option)
                    return resVerificacion
                else:
                    return ''
            else:
             return 'La selección no puede ser vacía'
        except Exception as e:
            print(f"Error en la ruta /validar_usuario: {str(e)}")
            return 'Error interno del servidor', 500

    # @app.route('/cerrar_inscripcion', methods=['POST', 'GET'])
    # def cerrar_inscripcion():
    #     idInscripcion = request.form.get('idInscripcion')

    #     return cerrarInscripcion(idInscripcion)

    @app.route('/cerrar_inscripcion/<idInscripcion>', methods=['POST', 'GET'])
    def cerrar_inscripcion(idInscripcion):

        return cerrarInscripcion(idInscripcion)
    
    @app.route('/verificar_cupo', methods=['POST','GET'])
    def verificar_cupo():
        inscripcion_id = request.form.get('inscripcion')
        materia_id = request.form.get('materia')

        if inscripcion_id and materia_id:
            verCupo(inscripcion_id, materia_id)
        else:
            return 'Error en la solicitud. Falta información.'