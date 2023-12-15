
#from mysql.connector import connect, Error
import mysql.connector

################### FUNCIONES PRINCIPALES ###################################

def conectarBD(configDB=None):
    """ Establecer una conexión con el servidor MySQL.
     Retorna la conexión """
    mydb=None
    if configDB!=None:
        try:        
            mydb = mysql.connector.connect(
                    host=configDB.get("host"),
                    user=configDB.get("user"),
                    password=configDB.get("pass"),
                    database=configDB.get("dbname")
                   )
        except mysql.connector.Error as e:
            print("ERROR ->",e)        
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
        print("ERROR ->",e)   
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

BASE={ "host":"localhost",
        "user":"root",
        "pass":"",
        "dbname":"base_prueba"}
