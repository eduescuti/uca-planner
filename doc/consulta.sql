use baseuca;

SELECT * FROM usuario;

SELECT * FROM inscripciones;

SELECT id, usuario, nombre, apellido, email, contraseña, rol 
FROM  usuario WHERE  email="eduescuti99@gmail.com" and contraseña="10101999";

/* Esto de arriba ya no funciona mas, porque borre la base de datos "base_prueba" */