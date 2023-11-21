
// AGREGAR FILA A TABLA
function agregarFila() {
  var nom = document.getElementById("mat").value;
  var com = document.getElementById("comi").value;

  var newTablaCurso = document.getElementById("tablaCurso");

  var newFila = newTablaCurso.insertRow(-1);

  var cell1 = newFila.insertCell(0);
  var cell2 = newFila.insertCell(1);
  var cell3 = newFila.insertCell(2);
  var cell4 = newFila.insertCell(3);

  cell1.innerHTML = "";
  cell2.innerHTML = com;
  cell3.innerHTML = nom;
  cell4.innerHTML = "";

  document.getElementById("ventana_1").style.display="none"
}

// VENTANA POPUP
function abrir() {
  document.getElementById("ventana_1").style.display = "grid";
}

function cerrar() {
  document.getElementById("ventana_1").style.display = "none";
}


function noSeleccionaCuatrimestre() {

  var cuatrimestre = document.getElementById("cuatrimestre").value;

  return (cuatrimestre == 0);
}

function fechasNoEstanSeleccionadas() {
  var fechaInicio = document.getElementById("inicioInscripcion").value;
  var fechaFin = document.getElementById("finInscripcion").value;

  return (fechaInicio == "") || (fechaFin == "");
}

function seleccionar(fecha, desde, hasta) {
  /* 
    Selecciona una parte de la fecha (pasada por parámetro como un string),
    elijiendo la posición desde dónde hasta dónde quiere seleccionar.
  */

  var seleccion = "";

  for (let i = desde; i < hasta; i++) {
    seleccion += fecha[i];
  }
  return seleccion;
}

function verificarAnio(inicio, fin) {
  /* 
    Verifica que el año de inicio de la inscripción sea igual al año de finalización
  */

  var anioInicio = seleccionar(inicio, 0, 4);
  var anioFin = seleccionar(fin, 0, 4);

  if (anioInicio == anioFin) {
    return true;
  }
  return false;
}

function verificarMes(inicio, fin) {
  /* 
    Verifica que el mes de inicio de la inscripción sea menor que el mes de finalización
  */
  var mesInicio = seleccionar(inicio, 5, 7);
  var mesFin = seleccionar(fin, 5, 7);

  if (mesInicio < mesFin) {
    return true;
  }
  return false;
}

function errorDeFechas() {
  /* 
    Verifica si existe alguna incompatibilidad con las fechas seleccionadas.
    (- Las fechas seleccionadas deben ser del mismo año)
    (- Las fechas seleccionadas deben tener los meses compatibles)

  */

  var fechaInicio = document.getElementById("inicioInscripcion").value;
  var fechaFin = document.getElementById("finInscripcion").value;
  var resultado;

  resultado = verificarAnio(fechaInicio, fechaFin);
  resultado = verificarMes(fechaInicio, fechaFin);

  return !resultado;
}

function validarDatos() {

  if (noSeleccionaCuatrimestre()) {
    alert("Debe seleccionar el cuatrimestre de las Inscripciones.");
    return false;

  } else if (fechasNoEstanSeleccionadas()) {
    alert("Debe seleccionar las fechas de INICIO y de FINALIZACIÓN de las Inscripciones.");
    return false;

  } else if (errorDeFechas()) {
    alert("Debe seleccionar fechas de INICIO y de FINALIZACIÓN compatibles.");
    return false;

  } else {
    return true;
  }
}

function eliminarError(id) {
  var horaElegida = document.getElementById(id).value;

  if (horaElegida > 0) {
      document.getElementById("errorhoras").innerHTML = "";
  } else {
      document.getElementById("errorhoras").innerHTML = "*Debe ingresar un rango horario de al menos algún día";
  }
}

function horasNoEstanSeleccionadas() {

  var horasLunes = document.getElementById("horas-lun").value;
  var horasMartes = document.getElementById("horas-mar").value;
  var horasMiercoles = document.getElementById("horas-mie").value;
  var horasJueves = document.getElementById("horas-jue").value;
  var horasViernes = document.getElementById("horas-vie").value;

  var faltanSeleccionarHoras = (horasLunes == "0" && horasMartes == "0"
      && horasMiercoles == "0" && horasJueves == "0" && horasViernes == "0");

  return faltanSeleccionarHoras;
}

function indicarQueFaltanCompletarCampos() {
  document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos";
}

function cupoNoValido(cupo) {
  return (cupo == "" || cupo < 1 || cupo > 100);
}

function validarCupo() {
  var cupo = document.getElementById("cupo").value;

  if (cupoNoValido(cupo)) {
      document.getElementById("errorcupo").innerHTML = "*Debe ingresar un cupo válido (MÍNIMO: 1, MÁXIMO: 100)"
  } else {
      document.getElementById("errorcupo").innerHTML = "";
  }
}

function validarDatos() {
  var cupo = document.getElementById("cupo").value;

  if (horasNoEstanSeleccionadas()) {
      indicarQueFaltanCompletarCampos();
      return false;

  } else if (cupoNoValido(cupo)) {
      indicarQueFaltanCompletarCampos();
      return false;

  } else {
      return true;
  }
}