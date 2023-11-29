''' Info:
    ACCESO A LOS DATOS
'''
from _mysql_db import *

""" 
==================
OBTENCION DE DATOS
==================
"""

def obtenerHorarios(dic):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    los rangos de horarios disponibles para poder cursar una materia.
    '''
    sQuery="""SELECT * FROM horas;"""
    lista = selectDB(BASE, sQuery)
    dic["horas"] = []
    for horas in lista:
        id, hora = horas
        dic["horas"].append({"id":id, "hora":hora })

def obtenerMaterias(dic):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    las materias y el codigo de las mismas.
    '''
    sQuery="""SELECT nombre, codigo FROM materias;"""
    lista = selectDB(BASE, sQuery)
    dic["materias"] = []
    for materia in lista:
        nombre, codigo = materia
        dic["materias"].append({"nombre":nombre, "codigo":codigo })

def obtenerComisiones(dic):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    todos los datos de las comisiones.
    '''
    sQuery="""SELECT * FROM comisiones;"""
    lista = selectDB(BASE, sQuery)
    dic["comisiones"] = []

    for comision in lista:
        id, nombre = comision
        dic["comisiones"].append({"id":id, "nombre":nombre})

    
def obtenerInfoTablaInscripciones(dic):
    select_inscripcion = """SELECT * FROM inscripciones;"""
    inscripciones = selectDB(BASE, select_inscripcion)
    """ [(id, estado, id_hora_mat, id_usuario), ...] """

    select_hora_mat_com = """SELECT * FROM hora_mat_com;"""
    hora_mat_com = selectDB(BASE, select_hora_mat_com)
    """ (id, id_com_mat, id_dia, id_hora) """

    select_mat_com = """SELECT * FROM materia_comision;"""
    mat_com = selectDB(BASE, select_mat_com)
    """ [(id, id_materia, id_comision, cupo), ..] """

    select_anio_comisiones = """SELECT DISTINCT año FROM comisiones;"""
    anios = selectDB(BASE, select_anio_comisiones)

    obtenerComisiones(dic)


    dic["infoTabla"] = {}
    dic["infoTabla"]["materias"] = []
    dic["infoTabla"]["inscripciones"] = []
    dic["infoTabla"] = []
    """ "materias" : [{"inscriptos" : { "usuarios" : ["eduescuti", "mariano", ...]}, "cupoMax" : 50, "materia" : Filosofia, "comision" : AM}],
        "inscripciones" : [{"estado" : "abierta", "año" : 2023, "cuatri" : 2}]

        algo asi deberia tener... para poder cargar los datos en la pagina de GestionInscripciones
    """
    


    for mat in mat_com:

        """ 
        select id from hora_mat_com

        cantidadInscriptos = 0;
        for id in id_hora_mat:
            for inscripcion in inscripciones:
                id_insc, estado, id_hora_mat_com, id_usuario = inscripcion
                if id_hora_mat_com == id:
                    cantidadInscriptos += 1

        Select count de los id_usuario que tengan id_hora_mat iguales (para contar los inscriptos)
        
        """

        id, nombre, comision, cupo = mat
        dic["infoTabla"]["infoMaterias"].append({"inscriptos" : 10, "materia" : nombre, "comision" : comision, "cupoMax" : cupo})


    

""" 
==================================================
INTERACCION USUARIO, OBTENCION DE DATOS DE USUARIO
==================================================
"""

def crearUsuario(di):
    '''### Información:
        Agrega un nuevo usuario (un registro) en la tabla usuario de la DB
        Recibe 'di' un diccionario con los datos del usuario a agegar en la tabla.
        Retorna True si realiza con existo el insert, False caso contrario.
    '''
    sQuery=""" 
        INSERT INTO usuario
        (id, usuario, nombre, apellido, email, contraseña, rol)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s);
    """
    val=(None, di.get('usuario'), di.get('nombre'), di.get('apellido'), di.get('email'), di.get('contraseña'), di.get('rol'))
    """ checkeo_usuario_valido(di.get('usuario'), di.get... lo que sea)
    
        PARA VALIDAR LOS DATOS
    """
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert==1

def obtenerUsuarioXEmail(param,email,clave='usuario'):
    '''### Información:
       Obtiene todos los campos de la tabla usuario en un dict a partir de la clave 'email'.
       Carga la información obtenida de la BD en el dict 'param'
       Recibe 'param' in diccionario
       Recibe 'email' que es el mail si se utiliza como clave en la búsqueda
       Recibe 'clave' que es a clave que se le colocará al dict 'param'
       
    '''
    sSql="""SELECT * FROM  usuario WHERE  email=%s;""" 
    val=(email,)

    fila=selectDB(BASE,sSql,val)
    param[clave]={}
    param[clave]['id']=fila[0][0]
    param[clave]['usuario']=fila[0][1]
    param[clave]['nombre']=fila[0][2]
    param[clave]['apellido']=fila[0][3]
    param[clave]['email']=fila[0][4]
    param[clave]['contraseña']=fila[0][5]
    param[clave]['rol']=fila[0][6]

def encuentraUnUsuario(result,user,password):
    '''### Información:
       Obtiene todos los campos de la tabla usuario a partir de la clave 'usuario'
         y del 'password'.
       Carga la información obtenida de la BD en el dict 'result'
       Recibe 'result' in diccionario donde se almacena la respuesta de la consulta
       Recibe 'user' que es el usuario si se utiliza como clave en la búsqueda
       Recibe 'password' que se utiliza en la consulta. (Para validadar al usuario)
       Retorna:
        True cuando se obtiene un registro de un usuario a partir del 'usuario' y el 'pass'.
        False caso contrario.
    '''
    res=False
    sSql="""SELECT id, usuario, nombre, apellido, email, contraseña, rol 
    FROM  usuario WHERE  usuario=%s and contraseña=%s;"""
    val=(user,password)
    fila=selectDB(BASE,sSql,val)
    if fila!=[]:
        res=True
        result['id']=fila[0][0]
        result['usuario']=fila[0][1]
        result['nombre']=fila[0][2]
        result['apellido']=fila[0][3]
        result['email']=fila[0][4] # es el mail
        result['contraseña']=fila[0][5]
        result['rol']=fila[0][6]
    return res

def actualizarPerfil(di, mail):
    """ Actualiza el perfil de un usuario pasandole por parámetro el mail,
    y un diccionario con los nuevos usuario, mail y contraseña.

    Devuelve True si se pudo actualizar, False en caso contrario.
    """
    sQuery="""UPDATE usuario 
        SET usuario=%s,
        email=%s,
        contraseña=%s 
        WHERE email=%s;
        """
    val=(di.get('usuario'), 
         di.get('email'), 
         di.get('contraseña'),
         mail)
    print(mail)
    print(val)
    print(di)
    
    resul_update=updateDB(BASE,sQuery,val=val)
    return resul_update==1

""" # def validarUsuario(email,password):
#     '''### Información:
#           Se consulta a la BD un usuario 'email' y un 'password'
#           retorna True si 'email' y  'password' son válido
#           retorna False caso contrario
#     '''
#     sSql='''
#         SELECT * FROM  usuario
#             WHERE 
#             email=%s
#             AND 
#             pass=%s;
#     '''
#     val=(email,password)
#     fila=selectDB(BASE,sSql,val=val)
#     return fila!=[] """

""" 
==========================
FUNCIONES DE ADMINISTRADOR
==========================
"""

def crearMateria(di):
    """ ### Agrega una materia en la base de datos 
    - Recibe un diccionario con la información del form
    (y agrega la materia con la info a la base)

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    insertMateria=""" 
        INSERT INTO materias
        (id, nombre, codigo)
        VALUES
        (%s,%s, %s);
    """
    val=(None, di.get('nombre'), di.get('codigo'))

    """ selectMaterias = "SELECT nombre, codigo FROM materias;"
    val2 = (di.get('nombre'), di.get('codigo'))
    lista = selectDB(BASE, selectMaterias, val2)
    if (lista == val2):
        return False
    else: 
        Esto es para ver si podemos indicar si ya existe en la base de datos los valores ingresados

        PODRIA SER UNA FUNCION DE VALIDACION ACA EN model.py
        
        """
    resul_insert=insertDB(BASE,insertMateria,val)
    return resul_insert==1

def crearComision(di):
    """ ### Agrega una comision en la base de datos 
    - Recibe un diccionario con la información del form
    (y agrega la materia con la info a la base)

    - Retorna True si realiza con existo el insert, False caso contrario.
    """

    sQuery=""" 
        INSERT INTO comisiones
        (id, nombre)
        VALUES
        (%s,%s);
    """
    val=(None, di.get('comision'))
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert==1

def crearInscripcion(di):
    """ ### Agrega una inscripcion en la base de datos 
    - Recibe un diccionario con la información del form
    (y agrega la materia con la info a la base)

    - Retorna True si realiza con existo el insert, False caso contrario.
    """

    sQuery=""" 
        INSERT INTO inscripciones
        (id, estado, año, cuatrimestre)
        VALUES
        (%s, %s, %s, %s);
    """
    val=(None, di.get('estado', di.get('anio'), di.get('cuatrimestre')))
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert==1

def hayHorarioEnDia(dia, di):
    """ ### Verifica si el administrador eligió un horario en dicho dia para el curso
    #### Se utiliza en la funcion "agregarDiasYHorarios()"
    - Recibe el diccionario del form pasado por parámetro, y el dia (como string)

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    return (di.get(dia) != "")

def seleccionarIDMateria(di):
    """ ### Realiza un SELECT para buscar el ID de la materia
    - Recibe el diccionario del form pasado por parámetro

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    select_id_materia="""
        SELECT id 
        FROM materias 
        WHERE codigo=%s;
    """
    val_materias = (di.get("mat"), )
    id_materia = selectDB(BASE, select_id_materia, val_materias)
    return id_materia[0][0]

def seleccionarIDComision(di):
    """ ### Realiza un SELECT para buscar el ID de la comision
    - Recibe el diccionario del form pasado por parámetro

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    select_id_comision="""
        SELECT id 
        FROM comisiones 
        WHERE nombre=%s;
    """
    val_comisiones = (di.get("comi"),)
    id_comision = selectDB(BASE, select_id_comision, val_comisiones)
    return id_comision[0][0]

def seleccionarUltimoIDMateria_Comision():
    """ ### Realiza un SELECT para buscar el último ID que aparece en la tabla "materia_comision" 

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    select_id_com_mat="""
        SELECT id 
        FROM materia_comision 
        ORDER BY id DESC LIMIT 1;
    """
    id_com_mat = selectDB(BASE, select_id_com_mat)
    return id_com_mat[0][0]

def seleccionarIDDia(dia):
    """ ### Realiza un SELECT para buscar el ID del dia
    - Recibe el dia (como string) por parámetro

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    select_id_dia="""
        SELECT id 
        FROM dias 
        WHERE dia=%s;
    """
    val_dia = (dia, )
    id_dia = selectDB(BASE, select_id_dia, val_dia)
    return id_dia[0][0]

def insertar_hora_mat_com(id_com_mat, id_dia, id_hora):
    """ ### Inserta el "curso" en la base de datos (en la tabla hora_mat_com)
    - Recibe id del curso (id_com_mat), el id del dia y el id_hora.

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    sQuery=""" 
        INSERT INTO hora_mat_com
        (id, id_com_mat, id_dia, id_hora)
        VALUES
        (%s, %s, %s, %s);
    """
    val = (None, id_com_mat, id_dia, id_hora)
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert

def agregarHorario(id_dia, id_hora):
    """ ### Agrega el dia y horario junto al curso en la base de datos 
    - Recibe un dicc con la información del form, el dia (como string)
    y el id_hora.

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    id_com_mat = seleccionarUltimoIDMateria_Comision()
    return insertar_hora_mat_com(id_com_mat, id_dia, id_hora)

def agregarDiasYHorarios(result, di):
    """ ### Agrega los dias y horarios de una materia_comision en la base de datos
    - Recibe un dicc con la información del form, y el resultado anterior de
    si se insertó bien la materia_comision.

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    if result==1:
        if (hayHorarioEnDia("lunes", di)):
            result = agregarHorario(seleccionarIDDia("lunes"), di.get("lunes"))
        
        if (hayHorarioEnDia("martes", di)):
            result = agregarHorario(seleccionarIDDia("martes"), di.get("martes"))
        
        if (hayHorarioEnDia("miercoles", di)):
            result = agregarHorario(seleccionarIDDia("miercoles"), di.get("miercoles"))
        
        if (hayHorarioEnDia("jueves", di)):
            result = agregarHorario(seleccionarIDDia("jueves"), di.get("jueves"))

        if (hayHorarioEnDia("viernes", di)):
            result = agregarHorario(seleccionarIDDia("viernes"), di.get("viernes"))

    return result

def insertar_materia_comision(di, id_materia, id_comision):
    """ ### Inserta una materia_comision en la base de datos 
    - Recibe un dicc con la información del form, el id_materia y id_comision

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    sQuery=""" 
        INSERT INTO materia_comision
        (id, id_materia, id_comision, cupo)
        VALUES
        (%s,%s, %s, %s);
    """
    val=(None, id_materia, id_comision, di.get('cupo'))
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert

def crear_materia_comision(di):
    """ ### Agrega una materia_comision en la base de datos 
    - Recibe un dicc con la información del form

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    id_materia = seleccionarIDMateria(di)
    id_comision = seleccionarIDComision(di)
    resul_insert = insertar_materia_comision(di, id_materia, id_comision)

    return agregarDiasYHorarios(resul_insert, di)