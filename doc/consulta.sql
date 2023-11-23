use baseuca;

SELECT * FROM usuario;

SELECT * FROM inscripciones;

SELECT id, usuario, nombre, apellido, email, contraseña, rol 
FROM  usuario WHERE  email="eduescuti99@gmail.com" and contraseña="10101999";

SELECT nombre, codigo FROM materias;

UPDATE usuario SET nombre="Eduardo" WHERE usuario="eduescuti"

UPDATE usuario SET rol="admin" WHERE usuario="mariano"

SELECT nombre, codigo FROM materias;

/* Esto de arriba ya no funciona mas, porque borre la base de datos "base_prueba" */