''' Info:
    ACCESO A LOS DATOS
'''
from _mysql_db import *


""" 
============================================
            OBTENCION DE DATOS
============================================
"""
def obtenerDias(dic):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    los dias disponibles para poder cursar una materia.
    
    dic["dias] = [{"id":1, "dia":"lunes"}, ...]
    '''
    sQuery="""SELECT * FROM dias;"""
    lista = selectDB(BASE, sQuery)
    dic["dias"] = []
    for dias in lista:
        id, dia = dias
        dic["dias"].append({"id":id, "dia":dia })

def obtenerHorarios(dic):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    los rangos de horarios disponibles para poder cursar una materia.
    
    dic["horas] = [{"id":1, "hora":"07:45-10:15hs"}, ...]
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

def obtenerCursos(dic):
    """ ### Obtiene TODOS los datos de los cursos de todas las inscripciones.
    Recibe un diccionario el cual se va a actualizar dentro cada curso

    Retorna el diccionario actualizado, se mostraría tal que:

    dic["cursos"] = [{"id_inscripcion":id_inscripcion,
                    "materia": {"nombre":nombre, "codigo":codigo, "comision":comision},
                    "inscriptos" : cantidadInscriptos,
                    "cupo": cupo,
                    "rango" : [{dia : hora}, {dia : hora}]}, ...]
    """
    sQuery="""SELECT DISTINCT id_inscripcion, id_com_mat FROM cursos;"""
    listaCursos = selectDB(BASE, sQuery)
    dic["cursos"] = []

    for curso in listaCursos:
        nuevoCurso = obtenerDatosCurso(curso)
        obtenerRangoHorario(nuevoCurso)
        dic["cursos"].append(nuevoCurso)

def obtenerCursosDisponibles(dic):
    """ ### Obtiene TODOS los datos de los cursos de la inscripcion dada que se encuentre 'Abierta'.
    Recibe un diccionario el cual se va a actualizar dentro cada curso

    Retorna el diccionario actualizado, se mostraría tal que:

    dic["cursos"] = [{"id_inscripcion":id_inscripcion,
                    "materia": {"nombre":nombre, "codigo":codigo, "comision":comision},
                    "inscriptos" : cantidadInscriptos,
                    "cupo": cupo,
                    "rango" : [{dia : hora}, {dia : hora}]}, ...]
    """
    sQuery="""SELECT DISTINCT id_inscripcion, id_com_mat FROM cursos;"""
    listaCursos = selectDB(BASE, sQuery)
    dic["cursos"] = []

    for curso in listaCursos:
        nuevoCurso = obtenerDatosCurso(curso)

        for inscripcion in dic["inscripciones"]:
            if ((inscripcion["id"] == nuevoCurso["id_inscripcion"]) and (inscripcion["estado"] == "abierta")):

                obtenerRangoHorario(nuevoCurso)
                dic["cursos"].append(nuevoCurso)

def obtenerInscripciones(dic):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    todos los datos de los períodos de inscripciones.
    '''
    sQuery="""SELECT * FROM inscripciones;"""
    lista = selectDB(BASE, sQuery)
    dic["inscripciones"] = []

    for inscripcion in lista:
        id, estado, anio, cuatri = inscripcion
        
        if (cuatri == 1):
            dic["inscripciones"].append({"id":id, "estado":estado, "año":anio, "cuatri":cuatri, "tipo":"er"})
        else:
            dic["inscripciones"].append({"id":id, "estado":estado, "año":anio, "cuatri":cuatri, "tipo":"do"})

def obtenerDatosCurso(curso):
    """ ### Obtiene los datos de los cursos (sin los horarios)
    - Recibe una tupla curso = (id_inscripcion, id_mat_com)
    - Devuelve un diccionario con los datos del curso
    """
    id_inscripcion, id_mat_com = curso
    nombre, codigo, comision = obtenerDatosMateriaComision(id_mat_com)
    cantidadInscriptos = obtenerCantidadInscriptos(id_inscripcion, id_mat_com)
    cupo = obtenerCupo(id_mat_com)
    nuevoCurso = {"id_inscripcion":id_inscripcion,
                  "materia": {"id_com_mat":id_mat_com, "nombre":nombre, "codigo":codigo, "comision":comision},
                  "inscriptos" : cantidadInscriptos,
                  "cupo": cupo}
    return nuevoCurso

def obtenerCantidadInscriptos(id_inscripcion, id_mat_com):
    ''' ### Obtiene la cantidad de inscriptos en un curso
    - Recibe el id_inscripcion y id_materia_comision.
    - Devuelve la cantidad de usuarios inscriptos en un curso (a la cantidad
    dada le resta uno porque cuenta también al administrador que creó el curso)
    '''
    select="""
        SELECT COUNT(DISTINCT id_usuario) 
        FROM cursos 
        WHERE id_inscripcion=%s and id_com_mat=%s;
    """
    val = (id_inscripcion, id_mat_com)
    listaCantidad = selectDB(BASE, select, val)
    
    return (listaCantidad[0][0] - 1)   #Le resta uno por el usuario del administrador que creó el curso

def obtenerCupo(id_mat_com):
    ''' ### Obtiene el cupo de una materia_comision
    - Recibe el id_com_mat
    - Devuelve el cupo máximo de la materia_comision
    '''
    select="""SELECT cupo FROM materia_comision WHERE id=%s;"""
    val = (id_mat_com, )
    listaCupo = selectDB(BASE, select, val)
    return listaCupo[0][0]

def obtenerHora(id_hora):
    ''' ### Obtiene un rango horario (las horas)
    - Recibe el id_hora
    - Devuelve el rango horario
    '''
    select_hora="""SELECT hora FROM horas WHERE id=%s;"""
    valHora = (id_hora, )
    listaHora = selectDB(BASE, select_hora, valHora)
    return listaHora[0][0]

def obtenerDia(id_dia):
    ''' ### Obtiene un dia
    - Recibe el id_dia
    - Devuelve el día
    '''
    select_dia="""SELECT dia FROM dias WHERE id=%s;"""
    valDia = (id_dia, )
    listaDia = selectDB(BASE, select_dia, valDia)
    return listaDia[0][0]

def seleccionarRangoHorarios(id_dia, id_hora):
    ''' ### Obtiene un dia y un rango horario
    - Recibe un id_dia y un id_hora
    - Devuelve el dia y la hora
    '''
    dia = obtenerDia(id_dia)
    hora = obtenerHora(id_hora)
    return dia, hora

def obtenerRangoHorario(curso):
    ''' ### Actualiza el curso con el rango horario
    - Recibe el diccionario con los datos del curso
    '''
    sQuery="""
        SELECT id_dia, id_hora 
        FROM cursos 
        WHERE id_inscripcion=%s and id_com_mat=%s;
    """
    val = (curso["id_inscripcion"], curso["materia"]["id_com_mat"])
    lista = selectDB(BASE, sQuery, val)
    curso["rango"] = []
    for rango in lista:
        id_dia, id_hora = rango
        dia, hora = seleccionarRangoHorarios(id_dia, id_hora)
        curso["rango"].append({"id_dia":id_dia, "dia":dia, "id_hora":id_hora, "hora" : hora})

def obtenerDatosMateria(id_materia):
    ''' ### Obtiene el nombre y el codigo de una materia
    - Recibe un id_materia
    - Devuelve el nombre y el código de una materia
    '''
    sQuery="""
        SELECT nombre, codigo
        FROM materias
        WHERE id=%s;
    """
    val=(id_materia, )
    lista = selectDB(BASE, sQuery, val)
    return lista[0][0], lista[0][1]

def obtenerNombreComision(id_comision):
    ''' ### Obtiene el nombre de una comision
    - Recibe un id_comision
    - Devuelve el nombre de la comisión
    '''
    sQuery="""
        SELECT nombre
        FROM comisiones
        WHERE id=%s;
    """
    val=(id_comision, )
    listaID = selectDB(BASE, sQuery, val)
    return listaID[0][0]

def obtenerDatosMateriaComision(id_com_mat):
    ''' Obtiene el nombre, codigo y comision de una materia
    - Recibe un id_comision_materia
    '''
    sQuery="""
        SELECT id_materia, id_comision
        FROM materia_comision
        WHERE id=%s;
    """
    val=(id_com_mat, )
    listaID = selectDB(BASE, sQuery, val)
    id_materia = listaID[0][0]
    id_comision = listaID[0][1]
    nombre, codigo = obtenerDatosMateria(id_materia)
    comision = obtenerNombreComision(id_comision)
    return nombre, codigo, comision

""" 
===========================================================
    INTERACCION USUARIO, OBTENCION DE DATOS DE USUARIO
===========================================================
"""
def esUsuarioValido(value):
    """ ### Verifica si se puede registrar el usuario
    - Recibe un value = (id, usuario, nombre, apellido, mail, contra, rol)
    - Devuelve True si el usuario es válido y False en caso contrario
    """
    checkeoMismoUsuario="""
        SELECT COUNT(*) 
        FROM usuario 
        WHERE usuario=%s;
    """
    val=(value[1], )
    usuarios=selectDB(BASE,checkeoMismoUsuario,val)
    cantidadUsuarios = usuarios[0][0]

    checkeoMismoMail="""
        SELECT COUNT(*) 
        FROM usuario 
        WHERE email=%s;
    """
    val=(value[4], )
    mails=selectDB(BASE,checkeoMismoMail,val)
    cantidadMail = mails[0][0]
    return ((cantidadUsuarios == 0) and (cantidadMail == 0))

def crearUsuario(di):
    '''### Crea el usuario y devuelve un booleano de si se pudo crear correctamente
    - Recibe el diccionario del request del form (y con esto crea el usuario)
    - Devuelve True si se pudo crear el usuario y False en caso contrario
    '''
    sQuery=""" 
        INSERT INTO usuario
        (id, usuario, nombre, apellido, email, contraseña, rol)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s);
    """
    val=(None, di.get('usuario'), di.get('nombre'), di.get('apellido'), di.get('mail'), di.get('contraseña'), di.get('rol'))
    if (esUsuarioValido(val)):
        resul_insert=insertDB(BASE,sQuery,val)
    else:
        resul_insert=0
    return resul_insert==1

def encuentraUnUsuario(result,user,password):
    '''### Información:
       Obtiene todos los campos de la tabla usuario a partir de la clave 'usuario' y del 'password' y
       carga la información obtenida de la BD en el dict 'result' (además devuelve true si encuentra un
       usuario con el usuario y la contraseña pasada por parametro)

       - Recibe 'result' in diccionario donde se almacena la respuesta de la consulta,
       'user' que es el usuario si se utiliza como clave en la búsqueda y
       'password' que se utiliza en la consulta. (Para validadar al usuario)

       - Retorna: True cuando se obtiene un registro de un usuario a partir del 'usuario' y el 'pass'.
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
    """ ### Actualiza el perfil del usuario
    - Recibe el diccionario del request del form del editar perfil
    - Devuelve True si se pudo actualizar, False en caso contrario.
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
    
    resul_update=updateDB(BASE,sQuery,val=val)
    return resul_update==1

""" 
==========================================================
           INICIO - FUNCIONES DE ADMINISTRADOR
==========================================================
"""

""" 
================================
FUNCIONES DE CREACION DE MATERIA
================================
"""
def esMateriaValida(value):
    """ ### Verifica si se puede agregar una materia
    - Recibe un value = (id, nombre, codigo)
    - Devuelve True si la materia es válida y False en caso contrario
    """
    checkeoMismoNombre="""
        SELECT COUNT(*)
        FROM materias
        WHERE nombre=%s;
    """
    val=(value[1], )
    nombres=selectDB(BASE,checkeoMismoNombre,val)
    cantidadNombresIguales = nombres[0][0]

    checkeoMismoCodigo="""
        SELECT COUNT(*)
        FROM materias
        WHERE codigo=%s;
    """
    val=(value[2], )
    codigos=selectDB(BASE,checkeoMismoCodigo,val)
    cantidadCodigosIguales = codigos[0][0]

    return ((cantidadNombresIguales == 0) and (cantidadCodigosIguales == 0))

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
    if esMateriaValida(val):
        resul_insert=insertDB(BASE,insertMateria,val)
    else:
        resul_insert=0
    return resul_insert==1

""" 
===================================
FUNCIONES DE CREACION DE COMISIONES
===================================
"""
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
    val=(None, (di.get('comision')).upper())     # Pone en mayúsculas la comisión
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert==1

""" 
===============================
FUNCIONES DE CREACION DE CURSOS
===============================
"""

def hayHorarioEnDia(dia, di):
    """ ### Verifica si el administrador eligió un horario en dicho dia para el curso
    #### Se utiliza en la funcion "agregarDiasYHorarios()"
    - Recibe el diccionario del form pasado por parámetro, y el dia (como string)

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    return (di.get(dia) != "")

def seleccionarIDMateria(di):
    """ ### Realiza un SELECT para buscar el ID de la materia a través del código de la materia
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
    """ ### Realiza un SELECT para buscar el ID de la comision a través del nombre de la comisión
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

def insertarCurso(id_inscripcion, id_com_mat, id_dia, id_hora, id_admin):
    """ ### Inserta el "curso" en la base de datos (en la tabla hora_mat_com)
    - Recibe id del curso (id_com_mat), el id del dia, el id_hora y 
    el id_admin (este lo utilizo para poder agregar el curso).

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    sQuery=""" 
        INSERT INTO cursos
        (id, id_inscripcion, id_com_mat, id_dia, id_hora, id_usuario)
        VALUES
        (%s, %s, %s, %s, %s, %s);
    """
    val = (None, id_inscripcion, id_com_mat, id_dia, id_hora, id_admin)
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert

def agregarHorario(id_dia, id_hora, id_inscripcion, id_admin):
    """ ### Agrega el dia, horario, la inscripcion y el administrador junto al curso en la base de datos 
    - Recibe un dicc con la información del form, el dia (como string)
    y el id_hora.

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    id_com_mat = seleccionarUltimoIDMateria_Comision()
    
    return insertarCurso(id_inscripcion, id_com_mat, id_dia, id_hora, id_admin)

def agregarDiasYHorarios(result, di, id_inscripcion, id_admin):
    """ ### Agrega los dias y horarios de una materia_comision en la base de datos
    - Recibe un dicc con la información del form, y el resultado anterior de
    si se insertó bien la materia_comision.

    - Retorna True si realiza con existo el insert, False caso contrario.
    """
    if result==1:
        if (hayHorarioEnDia("lunes", di)):
            id_dia = seleccionarIDDia("lunes")
            id_hora = di.get("lunes")
            result = agregarHorario(id_dia, id_hora, id_inscripcion, id_admin)
        
        if (hayHorarioEnDia("martes", di)):
            id_dia = seleccionarIDDia("martes")
            id_hora = di.get("martes")
            result = agregarHorario(id_dia, id_hora, id_inscripcion, id_admin)
        
        if (hayHorarioEnDia("miercoles", di)):
            id_dia = seleccionarIDDia("miercoles")
            id_hora = di.get("miercoles")
            result = agregarHorario(id_dia, id_hora, id_inscripcion, id_admin)
        
        if (hayHorarioEnDia("jueves", di)):
            id_dia = seleccionarIDDia("jueves")
            id_hora = di.get("jueves")
            result = agregarHorario(id_dia, id_hora, id_inscripcion, id_admin)

        if (hayHorarioEnDia("viernes", di)):
            id_dia = seleccionarIDDia("viernes")
            id_hora = di.get("viernes")
            result = agregarHorario(id_dia, id_hora, id_inscripcion, id_admin)

    return result

def esCursoValido(value):
    """ ### Verifica si se puede agregar el curso
    - Recibe un value = (id, id_materia, id_comision, cupo)
    - Devuelve True si el curso es válido y False en caso contrario
    """
    checkeo_misma_materia_comision="""
        SELECT COUNT(*)
        FROM materia_comision
        WHERE id_materia=%s and id_comision=%s;
    """
    val=(value[1], value[2])
    materia_comision=selectDB(BASE,checkeo_misma_materia_comision,val)
    cantidad_con_mismo_curso = materia_comision[0][0]

    return (cantidad_con_mismo_curso == 0)

def crearMateriaComision(di, id_materia, id_comision):
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
    if esCursoValido(val):
        resul_insert=insertDB(BASE,sQuery,val)
    else:
        resul_insert=0
    return resul_insert

def crearCurso(di, id_admin):
    """ ### Crea el curso en la base de datos
    - Recibe el diccionario del request del form y el id del admin (para poder ingresar a la base de datos,
    porque se necesita si o si de un id_usuario para poder insertar un curso a la base de datos)
    - Devuelve True si se pudo crear, False en caso contrario
    """
    id_materia = seleccionarIDMateria(di)
    id_comision = seleccionarIDComision(di)
    resul_insert = crearMateriaComision(di, id_materia, id_comision)
    id_inscripcion = di.get("inscripcion")

    return agregarDiasYHorarios(resul_insert, di, id_inscripcion, id_admin)

""" 
======================================
FUNCIONES DE PERIODO DE INSCRIPCIONES
======================================
"""

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
    val=(None, di.get('estado'), di.get('anio'), di.get('cuatrimestre'))
    resul_insert=insertDB(BASE,sQuery,val)
    print(resul_insert)
    print(resul_insert)
    print(resul_insert)
    return resul_insert==1

def cerrarIns(idIns, nuevoEstado):
    """ ### Cierra una inscripción
    - Recibe un id de una inscripción y el estado
    - Devuelve True si se pudo cerrar, False en caso contrario
    """
    try:
        connection = conectarBD(BASE)
        cursor = connection.cursor()

        # Realizar la actualización en la base de datos
        query = "UPDATE inscripciones SET estado = %s WHERE id = %s"
        cursor.execute(query, (nuevoEstado, idIns))
        connection.commit()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return True
    except Exception as e:
        # Manejar cualquier error
        return False, 'Error al cerrar la inscripción: ' + str(e)

""" 
=================================================
FUNCIONES DE INSCRIPCIÓN DE UN USUARIO A UN CURSO
=================================================
"""

def obtenerDiaHora(id_inscripcion, id_com_mat):
    ''' ### Obtiene el dia y el rango horario de un curso
    - Recibe un id_inscripcion y un id_comision_materia
    - Devuelve el id_dia y id_hora del curso
    '''
    sQuery="""
        SELECT id_dia, id_hora 
        FROM cursos 
        WHERE id_inscripcion=%s and id_com_mat=%s;
    """
    val = (id_inscripcion, id_com_mat)
    lista = selectDB(BASE, sQuery, val)
    id_dia = lista[0][0]
    id_hora = lista[0][1]
    return id_dia, id_hora

def usuarioEstaInscriptoACurso(value):
    ''' ### Verifica si un usuario está inscripto a un curso
    - Recibe un value = (id, id_inscripcion, id_com_mat, id_dia, id_hora, id_usuario)
    - Devuelve True si el usuario ya se inscribió, False en caso contrario
    '''
    sQuery="""
        SELECT COUNT(*)
        FROM cursos
        WHERE id_inscripcion=%s and id_com_mat=%s and id_usuario=%s;
    """
    val=(value[1], value[2], value[5])
    cantidad = selectDB(BASE, sQuery, val)
    return cantidad[0][0] > 0
    
def cupoDisponible(id_inscripcion, id_com_mat):
    """ ### Verifica si el cupo de un curso está disponible
    - Recibe el id_inscripcion y el id_comision_materia
    - Devuelve True si el cupo no alcanzó su máximo, False en caso contrario
    """
    cupoMaximo = obtenerCupo(id_com_mat)
    cantIns = obtenerCantidadInscriptos(id_inscripcion, id_com_mat)
    print(cantIns)
    print(cupoMaximo)
    return (cantIns < cupoMaximo)

def esPosibleInscribirseACurso(value):
    """ ### Verifica si un usuario puede inscribirse a un curso
    - Recibe un value = (id, id_inscripcion, id_com_mat, id_dia, id_hora, id_usuario)
    - Devuelve True si el usuario está habilitado para inscribirse, False en caso contrario
    """
    return (cupoDisponible(value[1], value[2]) and (not(usuarioEstaInscriptoACurso(value))))

def inscribirseACurso(di, id_usuario):
    """ ### Inscribe un alumno a un curso
    - Recibe el diccionario del request del form y el id del usuario
    - Devuelve True si se pudo inscribir el usuario, False en caso contrario
    """
    id_inscripcion = di["inscripcion"]
    id_com_mat = di["materia"]
    id_dia, id_hora = obtenerDiaHora(id_inscripcion, id_com_mat)
    sQuery=""" 
        INSERT INTO cursos
        (id, id_inscripcion, id_com_mat, id_dia, id_hora, id_usuario)
        VALUES
        (%s, %s, %s, %s, %s, %s);
    """
    val=(None, id_inscripcion, id_com_mat, id_dia, id_hora, id_usuario)
    
    if esPosibleInscribirseACurso(val):
        resul_insert=insertDB(BASE,sQuery,val)
    else:
        resul_insert=0
    return resul_insert==1

""" 
=============================================
 FUNCION DE VERIFICACIÓN DE SI EXISTE UN DATO
=============================================
"""

def verificar_existe(campo, query):
    """ ### Función de verificación de existencia de un valor dentro de una tabla de la DB
    - Recibe un campo (es decir, el valor por el cuál se va a buscar dentro de la DB) y la consulta query
    - Devuelve si existe el valor del campo en la base de datos
    """
    try:
        connection = conectarBD(BASE)
        cursor = connection.cursor()

        # Consulta para verificar la existencia del usuario
        cursor.execute(query, (campo,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()
        print(count)
        print(count>0)
        return count > 0

    except Exception as e:
        print(f'Error verificando existencia del user: {str(e)}')
        return False

""" 
==========================================================
             FIN - FUNCIONES DE ADMINISTRADOR
==========================================================
"""