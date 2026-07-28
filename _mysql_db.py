
#from mysql.connector import connect, Error
import os
import mysql.connector

# En local los datos de conexion se leen del archivo .env (no versionado).
# En Vercel las variables ya vienen del entorno, y load_dotenv() no las pisa.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

################### FUNCIONES PRINCIPALES ###################################

def conectarBD(configDB=None):
    """ Establecer una conexión con el servidor MySQL.
     Retorna la conexión """
    mydb=None
    if configDB!=None:
        try:
            params = dict(
                    host=configDB.get("host"),
                    port=configDB.get("port", 3306),
                    user=configDB.get("user"),
                    password=configDB.get("pass"),
                    database=configDB.get("dbname"),
                   )
            # TiDB Cloud (y cualquier MySQL gestionado) exige conexión TLS.
            if configDB.get("ssl"):
                import certifi
                params["ssl_ca"] = certifi.where()
                params["ssl_verify_identity"] = True
            mydb = mysql.connector.connect(**params)
        except mysql.connector.Error as e:
            # Sin conexion no hay nada que devolver: si se retorna None el error
            # aparece mucho despues y disfrazado (p.ej. 'NoneType' is not subscriptable).
            raise RuntimeError(
                "No se pudo conectar a la base de datos "
                "{user}@{host}:{port}/{dbname} (ssl={ssl}). "
                "Revisa las variables DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME y DB_SSL. "
                "Detalle: {err}".format(
                    user=configDB.get("user"),
                    host=configDB.get("host"),
                    port=configDB.get("port", 3306),
                    dbname=configDB.get("dbname"),
                    ssl=bool(configDB.get("ssl")),
                    err=e,
                )
            ) from e
    return mydb

def cerrarBD(mydb):
    """ Realiza el cierra un conexión a una base de datos.
    Recibe 'mydb' una conexion a una base de datos """
    if mydb!=None:
        mydb.close()

def consultarDB(mydb,sQuery="",val=None,title=False):
    """ Realiza la consulta 'SELECT'.

    Recibe 'myDataBase' una conexion a una base de datos,
    'sQuery' la cadena con la consulta sql,
    'val' tupla de valores separados anti sql injection y
    'title' booleana.

    Retorna una 'lista' con el resultado de la consulta
    cada fila de la 'lista' es una tupla.
    Si 'title' es True, entonces agrega a la lista
    los títulos de las columnas. """
    myresult=None
    try:
        if mydb!=None:
            mycursor = mydb.cursor()
            if val==None:
                mycursor.execute(sQuery)
            else:
                mycursor.execute(sQuery,val)
            myresult = mycursor.fetchall()
            # Para obtener los nombres de las columnas
            if title:
                myresult.insert(0,mycursor.column_names)
    except mysql.connector.Error as e:
        raise RuntimeError("Error al ejecutar la consulta: {err}\nSQL: {sql}".format(err=e, sql=sQuery.strip())) from e
    return myresult

def ejecutarDB(mydb,sQuery="",val=None):
    """ Realiza las consultas 'INSERT' 'UPDATE' 'DELETE'

    Recibe 'mydb' una conexion a una base de datos,
    'sQuery' la cadena con la consulta SQL (osea INSERT, UPDATE o DELETE) y
    'val' tupla de valores separados anti sql injection.
    
    Retorna la cantidad de filas afectadas con la query. """
    res=None
    try:
        mycursor = mydb.cursor()
        if val==None:
            mycursor.execute(sQuery)
        else:
            mycursor.execute(sQuery,val)
        mydb.commit()   
        res=mycursor.rowcount        # filas afectadas
    except mysql.connector.Error as e:
        mydb.rollback()
        # Aca no se relanza: las vistas ya interpretan res!=1 como "no se pudo guardar"
        # y muestran el mensaje de error correspondiente al usuario.
        print("ERROR ->",e)
    return res
    
############################################################################


## - - - FUNCIONES SECUNDARIAS - - - - - - - - - - - - - - - - - - - - - -
## UTILIZA LAS FUNCIONES PRINCIPALES PARA ACCEDER A LA BASE DE DATOS
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def selectDB(configDB=None,sql="",val=None,title=False):
    """ ### SELECT (devuelve una Lista)
    Recibe 'configDB' un 'dict' con los parámetros de conexion, 
    'sql' una cadena con la consulta sql,
    'val' valores separados anti sql injection y 
    'title' booleana.

    Retorna una 'list' con el resultado de la consulta cada fila de la 'list' es una 'tuple'.
    Si 'title' es True, entonces agrega a la lista
    los títulos de las columnas. """

    resQuery=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        resQuery=consultarDB(mydb,sQuery=sql,val=val,title=title)
        cerrarBD(mydb)
    return resQuery

def insertDB(configDB=None,sql="",val=None):
    """ ### INSERT
    Recibe 'configDB' un 'dict' con los parámetros de conexion
    , 'sql' una cadena con la consulta sql y 
    'val' tupla de valores separados anti sql injection """
    resQuery=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        resQuery=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return resQuery

def updateDB(configDB=None,sql="",val=None):
    """ ### UPDATE
    Recibe 'configDB' un 'dict' con los parámetros de conexion
    , 'sql' una cadena con la consulta sql y 
    'val' tupla de valores separados anti sql injection. """
    resQuery=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        resQuery=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return resQuery

def deleteDB(configDB=None,sql="",val=None):
    """ ### DELETE
    Recibe 'configDB' un 'dict' con los parámetros de conexion
    , 'sql' una cadena con la consulta sql y 
    'val' valores separados anti sql injection """
    resQuery=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        resQuery=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return resQuery

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## CONFIGURACION DE LA CONEXION A LA BASE DE DATOS
## DICCIONARIO con los datos de la conexión
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

BASE={ "host":   os.environ.get("DB_HOST", "localhost"),
        "port":   int(os.environ.get("DB_PORT", "3306")),
        "user":   os.environ.get("DB_USER", "root"),
        "pass":   os.environ.get("DB_PASS", ""),
        "dbname": os.environ.get("DB_NAME", "ucaplanner_base"),
        "ssl":    os.environ.get("DB_SSL", "false").lower() == "true"}
