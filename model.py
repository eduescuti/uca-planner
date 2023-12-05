''' Info:
    ACCESO A LOS DATOS
'''
from _mysql_db import *



""" 
==================
OBTENCION DE DATOS
==================
"""

""" 

obtencion de datos de los cursos de una inscripcion dada



"""

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
    """ ### Obtiene los datos de los cursos de cada período de inscripciones.
    Sirve para usar los datos en la página de Gestión de Inscripciones y para Cursos. 
    """
    sQuery="""SELECT id, id_inscripcion, id_com_mat FROM cursos;"""
    lista = selectDB(BASE, sQuery)
    dic["cursos"] = []
    for curso in lista:
        id, id_inscripcion, id_mat_com = curso
        nombre, codigo, comision = obtenerDatosMateriaComision(id_mat_com)
        cantidadInscriptos = obtenerCantidadInscriptos(id_inscripcion, id_mat_com)
        cupo = obtenerCupo(id_mat_com)

        dic["cursos"].append({"id":id, 
                              "id_inscripcion":id_inscripcion, 
                              "materia": {"nombre":nombre, "codigo":codigo, "comision":comision},
                              "inscriptos" : cantidadInscriptos,
                              "cupo": cupo})

    return dic

def obtenerInscripciones(dic):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    todos los datos de las comisiones.
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

def obtenerCantidadInscriptos(id_inscripcion, id_mat_com):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    la cantidad de inscriptos en un curso.

    Recibe el id_inscripcion y id_materia_comision para identificar cuántos alumnos hay inscriptos.
    '''
    select="""
        SELECT COUNT(*) AS cantidad 
        FROM cursos 
        WHERE id_inscripcion=%s and id_com_mat=%s;
    """
    val = (id_inscripcion, id_mat_com)
    listaCantidad = selectDB(BASE, select, val)
    return listaCantidad[0][0]

def obtenerCupo(id_mat_com):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    el cupo de una materia_comision.
    '''
    select="""SELECT cupo FROM materia_comision WHERE id=%s;"""
    val = (id_mat_com, )
    listaCupo = selectDB(BASE, select, val)
    return listaCupo[0][0]

def obtenerHora(id_hora):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    la hora.
    '''
    select_hora="""SELECT hora FROM horas WHERE id=%s;"""
    valHora = (id_hora, )
    listaHora = selectDB(BASE, select_hora, valHora)
    return listaHora[0][0]

def obtenerDia(id_dia):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    el dia.
    '''
    select_dia="""SELECT dia FROM dias WHERE id=%s;"""
    valDia = (id_dia, )
    listaDia = selectDB(BASE, select_dia, valDia)
    return listaDia[0][0]

def seleccionarRangoHorarios(id_dia, id_hora):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    las materias completas.
    '''
    dia = obtenerDia(id_dia)
    hora = obtenerHora(id_hora)
    return dia, hora

def obtenerDatosMateria(id_materia):
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    el nombre y el codigo de una materia.
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
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    el nombre de una comision.
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
    ''' Obtiene de la base de datos (en un dicc pasado por parámetro)
    el nombre y comision de una materia.
    '''
    sQuery="""
        SELECT id_materia, id_comision
        FROM materia_comision
        WHERE id=%s;
    """
    val=(id_com_mat, )
    listaID = selectDB(BASE, sQuery, val)
    print(listaID)
    id_materia = listaID[0][0]
    id_comision = listaID[0][1]
    nombre, codigo = obtenerDatosMateria(id_materia)
    comision = obtenerNombreComision(id_comision)
    return nombre, codigo, comision

def obtenerCantidadDeUsuariosEn(id_inscripcion, id_mat_com):
    sQuery="""
        SELECT COUNT(*) AS cantidad 
        FROM cursos 
        WHERE id_inscripcion=%s and id_com_mat=%s;
    """
    val=(id_inscripcion, id_mat_com)
    listaCantidad = selectDB(BASE, sQuery, val)
    return listaCantidad[0][0]

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
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert

def crearCurso(di, id_admin):
    id_materia = seleccionarIDMateria(di)
    id_comision = seleccionarIDComision(di)
    resul_insert = crearMateriaComision(di, id_materia, id_comision)
    id_inscripcion = di.get("inscripcion")

    return agregarDiasYHorarios(resul_insert, di, id_inscripcion, id_admin)

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
    return resul_insert==1

def inscribirseACurso(di, id_usuario):
    """ ### INSCRIBE un alumno a un curso
    - Recibe por parámetro un diccionario con el formRequest
    (tiene dentro la inscripcion que elije y... tiene que tener las materias que se inscribe... como hago para seleccionarlas?)
    
    """
    
    """ id_hora_mat = obtenerIDMateriasSeleccionadas(di)

    for hora_mat in id_hora_mat:
        insertCurso=""
            INSERT INTO cursos
            (id, id_hora_mat, id_usuario, id_inscripcion)
            VALUES
            (%s, %s, %s, %s);
        ""
        val=(None, hora_mat, id_usuario, di.get('inscripcion'))

    resul_insert=insertDB(BASE,insertCurso,val)
    return resul_insert==1 """


def verificar_existe(username):
    try:
        connection = conectarBD(BASE)
        cursor = connection.cursor()

        # Consulta para verificar la existencia del usuario
        query = 'SELECT COUNT(*) FROM usuario WHERE usuario = %s'
        cursor.execute(query, (username,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count > 0

    except Exception as e:
        print(f'Error verificando existencia del user: {str(e)}')
        return False
