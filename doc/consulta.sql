use baseuca;

/* SELECT DE CADA TABLA */

SELECT * FROM usuario;
SELECT * FROM dias;
SELECT * FROM horas;
SELECT * FROM materia_comision;
SELECT * FROM inscripciones;
SELECT * FROM hora_mat_com;
SELECT * FROM materias;
SELECT * FROM comisiones;
SELECT * FROM cursos;

/* -------------------- */


SELECT id, usuario, nombre, apellido, email, contraseña, rol 
FROM  usuario WHERE  email="eduescuti99@gmail.com" and contraseña="10101999";

SELECT nombre, codigo FROM materias;

UPDATE usuario SET nombre="Eduardo" WHERE usuario="eduescuti"

UPDATE usuario SET rol="admin" WHERE usuario="mariano"

SELECT nombre, codigo FROM materias;

SELECT * FROM comisiones;

INSERT INTO comisiones (nombre) VALUES ("BM");

SELECT id FROM materias WHERE codigo="450";


/* AGREGADO DE LOS DIAS A LA TABLA DIAS */
SELECT * FROM dias;
INSERT INTO dias (dia) VALUES ("lunes");
INSERT INTO dias (dia) VALUES ("martes");
INSERT INTO dias (dia) VALUES ("miercoles");
INSERT INTO dias (dia) VALUES ("jueves");
INSERT INTO dias (dia) VALUES ("viernes");


/* AGREGADO DE LAS HORAS A LA TABLA HORAS */
SELECT * FROM horas;
INSERT INTO horas (hora) VALUES ("07:45hs - 10:15hs");
INSERT INTO horas (hora) VALUES ("10:15hs - 12:15hs");
INSERT INTO horas (hora) VALUES ("11:30hs - 15:15hs");
INSERT INTO horas (hora) VALUES ("13:00hs - 15:15hs");
INSERT INTO horas (hora) VALUES ("14:00hs - 16:00hs");
INSERT INTO horas (hora) VALUES ("15:15hs - 17:15hs");
INSERT INTO horas (hora) VALUES ("17:15hs - 19:00hs");
INSERT INTO horas (hora) VALUES ("19:00hs - 21:00hs");


SELECT * FROM hora_mat_com;
ALTER TABLE horario_mat RENAME TO hora_mat_com;

SELECT id FROM materias WHERE codigo=450;

SELECT *
FROM usuario
ORDER BY id DESC
LIMIT 1;

use base_prueba;

SELECT COUNT(*) AS cantidad FROM hora_mat_com;

SELECT DISTINCT año FROM comisiones;

