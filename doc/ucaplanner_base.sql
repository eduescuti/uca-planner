-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-08-2024 a las 04:22:15
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ucaplanner_base`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comisiones`
--

CREATE TABLE `comisiones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(3) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_inscripcion` int(11) NOT NULL,
  `id_com_mat` int(30) NOT NULL,
  `id_dia` int(30) NOT NULL,
  `id_hora` int(30) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dias`
--

CREATE TABLE `dias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dia` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horas`
--

CREATE TABLE `horas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hora` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones`
--

CREATE TABLE `inscripciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estado` varchar(10) NOT NULL,
  `año` int(10) NOT NULL,
  `cuatrimestre` int(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `codigo` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materia_comision`
--

CREATE TABLE `materia_comision` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_materia` int(11) NOT NULL,
  `id_comision` int(11) NOT NULL,
  `cupo` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(30) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `contraseña` varchar(30) NOT NULL,
  `rol` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--
-- NOTA: las PRIMARY KEY y el AUTO_INCREMENT se declaran dentro de cada CREATE TABLE.
-- phpMyAdmin los agregaba despues con `ALTER TABLE ... MODIFY id ... AUTO_INCREMENT`,
-- pero TiDB no soporta agregar AUTO_INCREMENT a una columna ya creada (error 8200) y
-- esas sentencias fallaban en silencio, dejando el id sin autoincremento.

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD UNIQUE KEY `id_inscripcion` (`id_inscripcion`,`id_com_mat`,`id_dia`,`id_hora`,`id_usuario`),
  ADD KEY `id_com_mat` (`id_com_mat`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_dia` (`id_dia`),
  ADD KEY `id_hora` (`id_hora`);

--
-- Indices de la tabla `materia_comision`
--
ALTER TABLE `materia_comision`
  ADD UNIQUE KEY `id_materia` (`id_materia`,`id_comision`),
  ADD KEY `id_comision` (`id_comision`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD CONSTRAINT `cursos_ibfk_1` FOREIGN KEY (`id_inscripcion`) REFERENCES `inscripciones` (`id`),
  ADD CONSTRAINT `cursos_ibfk_2` FOREIGN KEY (`id_com_mat`) REFERENCES `materia_comision` (`id`),
  ADD CONSTRAINT `cursos_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `cursos_ibfk_4` FOREIGN KEY (`id_dia`) REFERENCES `dias` (`id`),
  ADD CONSTRAINT `cursos_ibfk_5` FOREIGN KEY (`id_hora`) REFERENCES `horas` (`id`);

--
-- Filtros para la tabla `materia_comision`
--
ALTER TABLE `materia_comision`
  ADD CONSTRAINT `materia_comision_ibfk_1` FOREIGN KEY (`id_comision`) REFERENCES `comisiones` (`id`),
  ADD CONSTRAINT `materia_comision_ibfk_2` FOREIGN KEY (`id_materia`) REFERENCES `materias` (`id`);

--
-- Datos de referencia
--
-- `dias` y `horas` son tablas fijas: la app las da por cargadas. Sin ellas,
-- `seleccionarIDDia`/`seleccionarIDHora` (model.py) fallan al armar un curso y
-- los selects de horarios de Cursos.html salen vacios.
--

INSERT INTO `dias` (`id`, `dia`) VALUES
(1, 'lunes'),
(2, 'martes'),
(3, 'miercoles'),
(4, 'jueves'),
(5, 'viernes');

INSERT INTO `horas` (`id`, `hora`) VALUES
(1, '07:45hs - 10:15hs'),
(2, '10:15hs - 12:15hs'),
(3, '11:30hs - 15:15hs'),
(4, '13:00hs - 15:15hs'),
(5, '14:00hs - 16:00hs'),
(6, '15:15hs - 17:15hs'),
(7, '17:15hs - 19:00hs'),
(8, '19:00hs - 21:00hs');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
