''' Info:
    ACCESO A LOS DATOS
'''
from _mysql_db import *


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
    """ checkeo_usuario_valido(di.get('usuario'), di.get... lo que sea) """
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

def actualizarUsuario(di,email):
    '''### Información:
        Actualiza el registro de la tabla usuario para la clave 'email'
        Recibe 'di' un dict con los campos que se requiere modificar.
        Recibe 'email' que es la clave para identificar el regsitro a actualizar.
        Retorna True si realiza la actualización correctamente.
                False caso contrario.

    '''
    sQuery="""update usuario 
        SET nombre=%s, 
        apellido=%s,
        pass=%s 
        WHERE email=%s;
        """
    val=(di.get('nombre'), 
         di.get('apellido'), 
         di.get('contraseña'), 
         email )
    
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

def crearMateria(di):
    """ ### Agrega una materia en la base de datos 
    - Recibe un diccionario con la información del form
    (y agrega la materia con la info a la base)

    - Retorna True si realiza con existo el insert, False caso contrario.
    """

    sQuery=""" 
        INSERT INTO materias
        (id, nombre, codigo)
        VALUES
        (%s,%s, %s);
    """
    val=(None, di.get('nombre'), di.get('codigo'))
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert==1

def crearComision(di):
    """ ### Agrega una comision en la base de datos 
    - Recibe un diccionario con la información del form
    (y agrega la materia con la info a la base)

    - Retorna True si realiza con existo el insert, False caso contrario.
    """

    sQuery=""" 
        INSERT INTO comisiones
        (id, nombre, año, cuatrimestre)
        VALUES
        (%s,%s, %s, %s);
    """
    print(di.get('comision'))
    val=(None, di.get('comision'), di.get('anio'), di.get('cuatrimestre'))
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert==1