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

def obtenerMensajeError(param, estado="carga exitosa"):
    param["error"] = {
        "error materia" : "No se pudo cargar la materia, porfavor intente denuevo..",
        "error comision" : "No se pudo cargar la comisión, porfavor intente denuevo..",
        "error curso" : "No se pudo cargar los datos del curso, porfavor intente denuevo..",
        "error inscripcion" : "No se pudo cargar los datos del período de inscripciones, porfavor intente denuevo.."
        }
    
    param["estado"] = estado

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
# + + I N I C I O + + MANEJO DE  SUBIDA DE ARCHIVOS  + + + + + + + + + + +
##########################################################################

def upload_file (diResult) :
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    MAX_CONTENT_LENGTH = 1024 * 1024     
    if request.method == 'POST' :         
        for key in request.files.keys():  
            diResult[key]={} 
            diResult[key]['file_error']=False            
            
            f = request.files[key] 
            if f.filename!="":     
                #filename_secure = secure_filename(f.filename)
                file_extension=str(os.path.splitext(f.filename)[1])
                filename_unique = uuid4().__str__() + file_extension
                path_filename=os.path.join( config['upload_folder'] , filename_unique)
                # Validaciones
                if file_extension not in UPLOAD_EXTENSIONS:
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: No se admite subir archivos con extension '+file_extension
                if os.path.exists(path_filename):
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: el archivo ya existe.'
                    diResult[key]['file_name']=f.filename
                try:
                    if not diResult[key]['file_error']:
                        diResult[key]['file_error']=True
                        diResult[key]['file_msg']='Se ha producido un error.'

                        f.save(path_filename)   
                        diResult[key]['file_error']=False
                        diResult[key]['file_name_new']=filename_unique
                        diResult[key]['file_name']=f.filename
                        diResult[key]['file_msg']='OK. Archivo cargado exitosamente'
 
                except:
                        pass
            else:
                diResult[key]={} # viene vacio el input del file upload

    # si existe el archivo devuelve True
    # os.path.exists(os.path.join('G:\\directorio\\....\\uploads',"agua.png"))

    # borrar un archivo
    # os.remove(os.path.join('G:\\directorio\\.....\\uploads',"agua.png"))
            
##########################################################################
# - - F I N - - MANEJO DE  SUBIDA DE ARCHIVOS  - - - - - - - - - - - - - - 
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
    obtenerMenuBottom(param)
    return render_template('IniciarSesion.html',param=param)

def register_pagina(param):
    '''
       Carga la pagina 'register'
    '''

    obtenerMenuBottom(param)       
    return render_template('Registrarse.html',param=param)

def cronograma_pagina(param):
    """Muestra la pantalla del visualizador
    """

    if haySesion():
        if (session["rol"] == "alumno"):
            obtenerInscripciones(param)
            obtenerCursosDisponibles(param)
            obtenerHorarios(param)

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
    '''Valida el usuario y el pass contra la BD.
    
    Recibe 'param' dict de parámetros y 
    'request' una solicitud http con los datos usuario y pass.

    Retorna: Si es valido el usuario y pass => crea una session y retorna la pagina home.
    Si NO es valido el usuario y pass => retorna la pagina login
    y agrega en el diccionario de parámetros una clave con un mensaje 
    de error para ser mostrada en la pagina login.
    '''
    
    if crearSesionUsuario(miRequest):
        res = redirect('/')
    else:
        res = redirect('/login')
    return res

def registrarUsuario(param, miRequest):
    '''info:
      Realiza el registro de un usuario en el sistema, es decir crea un nuevo usuario
      y lo registra en la base de datos.
      recibe 'param' el diccionario de parámetros.
      recibe request es la solicitud (post o get) proveniente del cliente
      retorna la pagina del login, para forzar a que el usuario realice el login con
      el usuario creado.
    '''
    obtenerMenuBottom(param)

    if crearUsuario(miRequest):
        param['succes_msg_login']="Se ha creado el usuario con exito"
        cerrarSesion()           # Cierra sesion existente(si la hubiere)
        res=login_pagina(param)  # Envia al login para que vuelva a loguearse el usuario
    else:
        param['error_msg_register']="Error: No se ha podido crear el usuario"
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


""" def actualizarDatosDeUsuarios(param, request):
    '''info:
            Recepciona la solicitud request que es enviada
            desde el formulario de edit_user 
          Retorna 
            si hay sesion: retorna la edit_user con los datos actualizados
               y un mensaje de exito o fracaso sobre el mismo form ; 
            si no hay sesion: retorna la home.
    '''
    res=False
    msj=""
    
    try:     
        getRequest(request)      
        # *** ACTUALIZAR USUARIO ***
        
        if actualizarUsuario(request, session.get("username")):
            res=True
            param['succes_msg_updateuser']="Se ha ACTUALIZADO el usuario con exito"
        else:
            #error
            res=False
            param['error_msg_updateuser']="Error: No se ha podido ACTUALIZAR el usuario"

        #editarUsuario_pagina(param)
        res= render_template('edit_user.html',param=param)  
    except ValueError as e :                   
        pass
    return res  """

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
# - - F I N - -   OTRAS PAGINAS    - - - - - - - - - - - - - - - - - - - -
##########################################################################

def agregarMateria(miRequest):
    """ Agrega una materia a la base de datos.
    Recibe el request del form de la página.
    """
    param={}    
    if haySesion():

        if (session["rol"] == "admin"):

            if crearMateria(miRequest):
                res = redirect('/materias')
            else:
                estado = "carga fallida"
                obtenerMensajeError(param, estado)
                res = materias_pantalla(param)

                """ De momento, NO recibe error dado que no realizo la validacion del dato ingresado
                con respecto a la Base de Datos.
                """

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
                res = redirect('/comisiones')

            else:
                estado = "carga fallida"
                obtenerMensajeError(param, estado)
                res = comisiones_pantalla(param)
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
                obtenerMensajeError(param, estado)
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
                obtenerMensajeError(param, estado)
                res = gestion_inscripciones_pantalla(param)
    else:
        res = redirect('/')
    return res


def inscribirse(miRequest):
    param={}
    if haySesion():

        if (session["rol"] == "alumno"):

            if inscribirseACurso(miRequest, session["id"]):
                res = redirect('/cronograma')

            else:
                estado = "carga fallida"
                obtenerMensajeError(param, estado)
                res = cronograma_pagina(param)
    else:
        res = redirect('/')
    return res


def verUsuario(username):
    if verificar_existe(username)==True:
        return 'El nombre de usuario ya existe.'
    else:
        return 'El nombre de usuario está disponible.'
    

def verEstado(option):
    if verificarExiste(option)==True:
        return 'Ya existe una inscripción abierta'
    else:
        return ''