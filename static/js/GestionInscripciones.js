// ESTO YA NO SIRVE
// // AGREGAR FILA A TABLA
// function agregarFila() {
//   var nom = document.getElementById("mat").value;
//   var com = document.getElementById("comi").value;
//   var cupo = document.getElementById("cupo").value;

//   var newTablaCurso = document.getElementById("tablaCurso");

//   var newFila = newTablaCurso.insertRow(-1);

//   var cell1 = newFila.insertCell(0);
//   var cell2 = newFila.insertCell(1);
//   var cell3 = newFila.insertCell(2);
//   var cell4 = newFila.insertCell(3);

//   cell1.innerHTML = "";
//   cell2.innerHTML = com;
//   cell3.innerHTML = nom;
//   cell4.innerHTML = "";

//   document.getElementById("ventana_1").style.display = "none"
// }

// // VENTANA POPUP
// function abrir() {
//   document.getElementById("ventana_1").style.display = "grid";
// }

// function cerrar() {
//   document.getElementById("ventana_1").style.display = "none";
// }


/*===================================
  ------- VALIDACION DE DATOS ------- 
  -----------------------------------
*/

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
  document.getElementById("error_incompleto").innerHTML = "*Debe completar todos los campos";
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


function filtrarTabla() {
  // obtiene valor del input
  var filtro = document.getElementById('inputFiltro').value.toLowerCase();
  // obtiene todas las filas de la tabla
  var filas = document.getElementById('tablaCurso').getElementsByTagName('tbody')[0].getElementsByTagName('tr');

  // recorre todas las filas de la tabla
  for (var i = 0; i < filas.length; i++) {
    // obtiene la fila actual
    var fila = filas[i];
    // obtiene todas las celdas de la fila
    var celdas = fila.getElementsByTagName('td');
    // variable que indica si hay coincidencia o no
    var coincide = false;

    // recorre cada celda
    for (var j = 0; j < celdas.length; j++) {
      // toma celda actual
      var dato = celdas[j];
      // Compara el contenido de la celda con el filtro (ignorando mayúsculas)
      if (dato.textContent.toLowerCase().includes(filtro)) {
        coincide = true; //si la coincidencia existe cambia la variable a true
        break;
      }
    }

    fila.style.display = coincide ? '' : 'none'; //muestra u oculta la fila en caso de que coincida o no
  }

}

//coincide ? '' : 'none'    coincide ? (true) : (false)
// si es true sera una cadena vacia si es false sera none 