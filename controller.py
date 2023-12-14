'''### info:
     CONTROL 
'''
from flask import request, session, redirect, render_template, jsonify
from model import *
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from appConfig import config


def obtenerInformacionPerfil(param):
    
    param["usuario"] = session['usuario']
    param["nombre"] = session['nombre']
    param["apellido"] = session['apellido']
    param["email"] = session['email']
    param["rol"] = session['rol']

def obtenerMenuBottom(param, idActivo="mnub01"):
    '''info:
    Carga el dict 'param' con las datos de un menu
    que será utilizado para cargar un html.
    Recibe  'idActivo' Es el id del diccionario de aquel item del menu que estará 
    marcado en el html como activo.
    Recibe 'param' el diccionario de parámetros. 
    '''

    param["page-title"]=""
    param["page-header"]=""
    
    param["menubottom"]= {
            "mnub01":{"href":"/home","content":"Home","class":" "},
            "mnub02":{"href":"/login","content":"Log In","class":" "},
            "mnub03":{"href":"/register","content":"Register","class":" "},
            "mnub04":{"href":"/registerAdmin","content":"Admin Register","class":" "},
            "mnub05":{"href":"/cronograma","content":"Cronograma","class":" "},
            "mnub06":{"href":"/materias","content":"Materias","class":" "},

            "mnub07":{"href":"/edit_user","content":"Editar Usuario","class":" "}
        }
    # Activar el id 
    param["menubottom"].get(idActivo)["class"]="active"

def obtenerMensajes(param):
    param["error"] = {
        "comision" : "No se pudo cargar la comisión, porfavor intente denuevo..",
        "curso" : "No se pudo cargar los datos del curso, porfavor intente denuevo..",
        "cupoExcedido": "Lo sentimos, el cupo para esta materia ha sido excedido."
    }
    param["comision_agregada"] = ""
    param["materia_agregada"] = ""
    param["inscripcion_exitosa"] = ""
    param["ingrese_usuario_valido"] = ""
    param["mensaje_registro_exitoso"] = ""

##########################################################################
# + + I N I C I O + + MANEJO DE  REQUEST + + + + + + + + + + + + + + + + +
##########################################################################

def getRequest(diccionario):
    """
        Actualiza el diccionario ingresado por parámetro con los datos del form 
        Los guarda con { "name" : "value" } (siendo name y value los atributos de las etiquetas en el HTML)
    """
    if request.method=='POST':
        for name in request.form.to_dict().keys():
            lista = request.form.getlist(name)
            if len(lista)>1:
                diccionario[name]=request.form.getlist(name)
            elif len(lista)==1:
                diccionario[name]=lista[0]
            else:
                diccionario[name]=""

    elif request.method=='GET':  
        for name in request.args.to_dict().keys():
            lista=request.args.getlist(name)
            if len(lista)>1:
                diccionario[name]=request.args.getlist(name)
            elif len(lista)==1:
                diccionario[name]=lista[0]
            else:
                diccionario[name]=""     

##########################################################################
# - - F I N - - MANEJO DE  REQUEST - - - - - - - - - - - - - - - - - - - -
##########################################################################


##########################################################################
# + + I N I C I O + + MANEJO DE  SESSION + + + + + + + + + + + + + + + + +
##########################################################################

def cargarSesionUsuario(dicUsuario):
    '''info:
        Realiza la carga de datos del usuario
        en la variable global dict 'session'.
        recibe 'dicUsuario' que es un diccionario con datos
               de un usuario 
    '''

    session['id'] = dicUsuario['id']
    session['usuario'] = dicUsuario['usuario']
    session['nombre'] = dicUsuario['nombre']
    session['apellido'] = dicUsuario['apellido']
    session['email'] = dicUsuario['email']
    session['contraseña'] = dicUsuario['contraseña']
    session['rol'] = dicUsuario['rol']
    
def crearSesionUsuario(mirequest):
    '''info:
        Crea una sesion. Consulta si los datos recibidos son validos.
        Si son validos cargar una sesion con los datos del usuario
        recibe 'request' una solicitud htpp con los datos 'email' y 'pass' de un usuario
        retorna True si se logra un session, False caso contrario
    '''
    sesionValida=False
    try:
        # CONSULTA A LA BASE DE DATOS, Si usuario es valido => crea session
        dicUsuario={}
        if encuentraUnUsuario(dicUsuario,mirequest.get("usuario"),mirequest.get("contraseña")):
            # Carga sesion (Usuario validado)
            cargarSesionUsuario(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

def haySesion():  
    '''info:
        Determina si hay una sesion activa observando si en el dict
        session se encuentra la clave 'username'
        retorna True si hay sesión y False si no la hay.
    '''
    return session.get("usuario")!=None

def cerrarSesion():
    '''info:
        Borra el contenido del dict 'session'
    '''
    try:    
        session.clear()
    except:
        pass

##########################################################################
# - - F I N - - MANEJO DE  SESSION - - - - - - - - - - - - - - - - - - - -
##########################################################################


##########################################################################
# + + I N I C I O + + PAGINAS DE UCA PLANNER   + + + + + + + + + + + + + +
##########################################################################

def home_pagina(): 
    '''
      Carga la pagina home.
      Recibe 'param' el diccionario de parametros
      Retorna la pagina 'home'
    '''

    if haySesion():
        if (session['rol']== 'alumno'):
            return render_template('MenuPrincipalUsuario.html')
        else:
            return render_template('MenuPrincipalAdmin.html')
    else:
        return render_template('MenuPrincipal.html')

def login_pagina(param):
    '''
      Carga la pagina login.
      Recibe 'param' el diccionario de parametros
      Retorna la pagina 'login'
    '''
    return render_template('IniciarSesion.html',param=param)

def register_pagina(param):
    '''
       Carga la pagina 'register'
    '''      
    return render_template('Registrarse.html',param=param)

def cronograma_pagina(param):
    """Muestra la pantalla del visualizador
    """

    if haySesion():
        if (session["rol"] == "alumno"):
            obtenerInscripciones(param)
            obtenerCursosDisponibles(param)
            obtenerHorarios(param)
            obtenerDias(param)

            return render_template("OrganizadorDeHorarios.html", param=param)
    
    return render_template("Visualizador.html")

def perfil_pagina(param):
    """Dependiendo de si hay sesión iniciada o no, devuelve la página
    del usuario o administrador (en caso de estar iniciado sesión) o devuelve
    una página no encontrada como mensaje.
    """
    obtenerInformacionPerfil(param)

    if haySesion():
        if (session['rol'] == 'alumno'):
            return render_template("Usuario.html", param=param)
        else:
            return render_template("Administrador.html", param=param)
    
    return redirect('/')

def inscripciones_pantalla(param):
    
    obtenerInscripciones(param)

    if haySesion():

        if (session["rol"] == "admin"):
            return render_template("Inscripciones.html", param=param)
        
    return redirect('/')

def gestion_inscripciones_pantalla(param):

    obtenerInscripciones(param)
    obtenerCursos(param)

    if haySesion():

        if (session["rol"] == "admin"):
            return render_template("GestionInscripciones.html", param=param)
        
    return redirect('/')

def materias_pantalla(param):

    obtenerMaterias(param)
    
    if haySesion():

        if (session["rol"] == "admin"):
            return render_template("Materias.html", param=param)
        
    return redirect('/')

def comisiones_pantalla(param):

    obtenerComisiones(param)
    
    if haySesion():

        if (session["rol"] == "admin"):
            return render_template("Comisiones.html", param=param)
        
    return redirect('/')

def cursos_pantalla(param):

    obtenerInscripciones(param)
    obtenerCursos(param)
    obtenerMaterias(param)
    obtenerComisiones(param)
    obtenerHorarios(param)

    if haySesion():

        if (session["rol"] == "admin"):
            return render_template("Cursos.html", param=param)
        
    return redirect('/')


##########################################################################
# - - F I N - - PAGINA home, main y login  - - - - - - - - - - - - - - - -
##########################################################################


##########################################################################
# + + I N I C I O + + USUARIO: registro, edicion, actualizacion  + + + + + 
##########################################################################

def ingresoUsuarioValido(miRequest):
    '''Valida el usuario y el pass con la BD (se utiliza para iniciar sesión).
    
    Recibe 'param' dict de parámetros y 
    'request' una solicitud http con los datos usuario y pass.

    Retorna: Si es valido el usuario y pass => crea una session y retorna la pagina home.
    Si NO es valido el usuario y pass => retorna la pagina login
    y agrega en el diccionario de parámetros una clave con un mensaje 
    de error para ser mostrada en la pagina login.
    '''
    param={}
    if crearSesionUsuario(miRequest):
        res = redirect('/')
    else:
        obtenerMensajes(param)
        param["ingrese_usuario_valido"] = "*Ingrese un usuario y contraseña válidos.."
        res = login_pagina(param)
    return res

def registrarUsuario(miRequest):
    '''info:
      Realiza el registro de un usuario en el sistema, es decir crea un nuevo usuario
      y lo registra en la base de datos.
      recibe 'param' el diccionario de parámetros.
      recibe request es la solicitud (post o get) proveniente del cliente
      retorna la pagina del login, para forzar a que el usuario realice el login con
      el usuario creado.
    '''
    param={}
    if crearUsuario(miRequest):
        param['mensaje_registro_exitoso']="Inicie la sesión con su usuario creado:"
        cerrarSesion()           # Cierra sesion existente(si la hubiere)
        res=login_pagina(param)  # Envia al login para que vuelva a loguearse el usuario
    else:
        res=register_pagina(param)
    return res 

def editarPerfil_pagina(param):
    '''info:
        Carga la pagina edit_user
        Retorna la pagina edit_user, si hay sesion; sino retorna la home.
    '''
    obtenerInformacionPerfil(param)
    res = redirect('/')

    if haySesion():
        if (session["rol"] == "alumno"):
            res = render_template("EditarPerfil.html", param=param)
        else:
            res = render_template("EditarPerfilAdmin.html", param=param)
           
    return res  

def editarPerfil(miRequest):
    """ Se encarga de editar el perfil con los datos ingresados por parametro.
    """
    print(miRequest)
    if actualizarPerfil(miRequest, session['email']):

        session['usuario'] = miRequest.get('usuario')
        session['email'] = miRequest.get('email')
        session['contraseña'] = miRequest.get('contraseña')
    
    return redirect('/perfil')


##########################################################################
# - - F I N - - USUARIO: registro, edicion, actualizacion  - - - - - - - -
##########################################################################


##########################################################################
# + + I N I C I O + +  OTRAS PAGINAS     + + + + + + + + + + + + + + + + +
##########################################################################

def paginaNoEncontrada(name):
    ''' Info:
      Retorna una pagina generica indicando que la ruta 'name' no existe
    '''
    res='Pagina "{}" no encontrada<br>'.format(name)
    res+='<a href="{}">{}</a>'.format("/","Home")
    
    return res

##########################################################################
# - - FUNCIONES DE  INTERACCION    - - - - - - - - - - - - - - - - - - - -
##########################################################################

def agregarMateria(miRequest):
    """ Agrega una materia a la base de datos.
    Recibe el request del form de la página.
    """
    param={}
    obtenerMensajes(param)
    if haySesion():

        if (session["rol"] == "admin"):

            if crearMateria(miRequest):
                param["materia_agregada"] = "*La materia fue agregada con éxito!"
                res = materias_pantalla(param)
            else:
                res = redirect('/materias')
    else:
        res = redirect('/')
    return res

def agregarComision(miRequest):
    """ Agrega una comision a la base de datos.
    Recibe el request del form de la página.
       """
    param={}
    if haySesion():

        if (session["rol"] == "admin"):

            if crearComision(miRequest):
                param["comision_agregada"] = "La comisión fue creada con éxito!"
                res = comisiones_pantalla(param)

            else:
                res = redirect('/comisiones')
    else:
        res = redirect('/')
    return res

def agregarCurso(miRequest):
    """ Agrega una comision a la base de datos.
    Recibe el request del form de la página.
       """
    param={}
    if haySesion():

        if (session["rol"] == "admin"):

            if crearCurso(miRequest, session["id"]):
                res = redirect('/cursos')

            else:
                estado = "carga fallida"
                obtenerMensajes(param, estado)
                res = cursos_pantalla(param)
    else:
        res = redirect('/')
    return res

def agregarInscripcion(miRequest):
    param={}
    if haySesion():

        if (session["rol"] == "admin"):

            if crearInscripcion(miRequest):
                res = redirect('/gestion_inscripciones')

            else:
                estado = "carga fallida"
                obtenerMensajes(param, estado)
                res = gestion_inscripciones_pantalla(param)
    else:
        res = redirect('/')
    return res

def inscripcion_usuario(miRequest):
    param={}
    if haySesion():

        if (session["rol"] == "alumno"):
            
            if inscribirseACurso(miRequest, session["id"]):
                param["inscripcion_exitosa"] = "Inscripción realizada con éxito!"
                res = cronograma_pagina(param)
            else:
                res = redirect('/cronograma')
            
    else:
        res = redirect('/')
    return res


def verUsuario(username):
    query = 'SELECT COUNT(*) FROM usuario WHERE usuario = %s'
    if verificar_existe(username, query)==True:
        return '*El nombre de usuario ya existe.'
    else:
        return ''
    
def verEmail(email):
    query = 'SELECT COUNT(*) FROM usuario WHERE email = %s'
    if verificar_existe(email, query)==True:
        return '*El email ya está en uso.'
    else:
        return ''
    
def verEstado(option):
    query = 'SELECT COUNT(*) FROM inscripciones WHERE estado = %s'
    if verificar_existe(option, query)==True:
        return '*Ya existe una inscripción abierta'
    else:
        return ''

def verCupo(inscripcionId, materiaId):
    cupoMaximo = obtenerCupo(materiaId)
    cantIns = obtenerCantidadInscriptos(inscripcionId, materiaId)

    if (cantIns > (cupoMaximo + 1)):

        return "No se puede inscribir a dicha materia, el cupo está exedido."
    else:    
        return ""

def verNombreMateria(nombre):
    query = 'SELECT COUNT(*) FROM materias WHERE nombre = %s'
    if verificar_existe(nombre, query)==True:
        return '*El nombre de la materia ya existe, ingrese otro'
    else:
        return ''

def verCodigoMateria(codigo):
    query = 'SELECT COUNT(*) FROM materias WHERE codigo = %s'
    if verificar_existe(codigo, query)==True:
        return '*Ya existe un codigo creado con ese valor, ingrese otro'
    else:
        return ''

def verComision(comision):
    query = 'SELECT COUNT(*) FROM comisiones WHERE nombre = %s'
    if verificar_existe(comision, query)==True:
        return '*El nombre de esta comision ya existe, ingrese otro'
    else:
        return ''

def cerrarInscripcion(idIns):
    try:
        success = cerrarIns(idIns, 'cerrada')

        if success:
            return 'Inscripción cerrada exitosamente (recargue la página para ver el cambio de estado)'
        else:
            return 'Error al intentar cerrar la inscripción. Por favor, inténtalo nuevamente.'
    except Exception as e:
        # Captura cualquier excepción inesperada para evitar que la aplicación falle
        print(f'Error al cerrar la inscripción: {str(e)}')
        return 'Ocurrió un error inesperado al cerrar la inscripción.'

