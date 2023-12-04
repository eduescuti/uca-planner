
// AGREGAR FILA A TABLA
function agregarFila() {
  var nom = document.getElementById("mat").value;
  var com = document.getElementById("comi").value;
  var cupo = document.getElementById("cupo").value;

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

  document.getElementById("ventana_1").style.display = "none"
}

// VENTANA POPUP
function abrir() {
  document.getElementById("ventana_1").style.display = "grid";
}

function cerrar() {
  document.getElementById("ventana_1").style.display = "none";
}


/*===================================
  ------- VALIDACION DE DATOS ------- 
  -----------------------------------
*/

function eliminarError(id) {
  var horaElegida = document.getElementById(id).value;

  if (horaElegida > 0) {
    document.getElementById("errorhoras").innerHTML = "";
  } else {
    document.getElementById("errorhoras").innerHTML = "*Debe ingresar un rango horario de al menos algún día";
  }
}

function noSelecciona(campo) {
  return (campo == "")
}

function cupoNoValido(cupo) {
  return (cupo == "" || cupo < 1 || cupo > 100);
}

function horasNoEstanSeleccionadas() {

  var horasLunes = document.getElementById("horas-lun").value;
  var horasMartes = document.getElementById("horas-mar").value;
  var horasMiercoles = document.getElementById("horas-mie").value;
  var horasJueves = document.getElementById("horas-jue").value;
  var horasViernes = document.getElementById("horas-vie").value;

  var faltanSeleccionarHoras = (noSelecciona(horasLunes) && noSelecciona(horasMartes)
    && noSelecciona(horasMiercoles) && noSelecciona(horasJueves) && noSelecciona(horasViernes));

  return faltanSeleccionarHoras;
}

function indicarQueFaltanCompletarCampos() {
  document.getElementById("errorhoras").innerHTML = "*Debe completar todos los campos";
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
  var materia = document.getElementById("mat").value;
  var comision = document.getElementById("comi").value;
  var cupo = document.getElementById("cupo").value;

  if (noSelecciona(inscripcion)) {
    indicarQueFaltanCompletarCampos();
    return false;

  } else if (noSelecciona(materia)) {
    indicarQueFaltanCompletarCampos();
    return false;

  } else if (noSelecciona(comision)) {
    indicarQueFaltanCompletarCampos();
    return false;

  } else if (cupoNoValido(cupo)) {
    indicarQueFaltanCompletarCampos();
    return false;

  } else if (horasNoEstanSeleccionadas()) {
    indicarQueFaltanCompletarCampos();
    return false;

  } else {
    return true;
  }
}

function obtenerAnioActual() {
  var x = new Date();

  return x.getFullYear();
}

function insertarAnioActual() {

  var anio = obtenerAnioActual();

  document.getElementById("anio").value = anio;
}

function anioNoValido(anio) {
  return anio < (obtenerAnioActual());
}

function noEsValidoEl(campo) {
  return campo == "0";
}

function validarAnio() {
  var anio = document.getElementById("anio").value;

  if (anioNoValido(anio)) {
      document.getElementById("error anio").innerHTML = "*Ingrese un año válido";
  } else {
      document.getElementById("error anio").innerHTML = "";
  }
}

function indicarQueFaltanCompletarCampos() {
  document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos";
}

function validarDatos() {
  var estado = document.getElementById("estado").value;
  var anio = document.getElementById("anio").value;
  var cuatrimestre = document.getElementById("cuatrimestre").value;

  if (anioNoValido(anio)) {
      indicarQueFaltanCompletarCampos();
      return false;

  } else if (noEsValidoEl(cuatrimestre)) {
      indicarQueFaltanCompletarCampos();
      return false;

  } else if (noEsValidoEl(estado)) {
      indicarQueFaltanCompletarCampos();
      return false;

  } else {
      return true;
  }
}