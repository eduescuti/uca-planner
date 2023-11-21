from os import path 
config={}
# Directorio del proyecto
config['project_folder'] = path.dirname(path.realpath(__file__))
# directorio para subir archivos (con el path completo.
config['upload_folder']  = path.join( config['project_folder'] ,'uploads')