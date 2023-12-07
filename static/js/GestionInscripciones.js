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



function validarEstado(){
  var selectEstado = document.getElementById('estado');
  var option = selectEstado.value.trim(); // Obtiene el valor seleccionado en el select
  var boton = document.getElementById('btnInscripciones');


  queryAjaxForm('/validar_estado/' + option , 'res', 'formInscripciones')
}

function queryAjaxForm(url, idDest, idForm, method = "POST") {
  var formData = getDataForm(idForm);
  var xhr = conectAjax();

  if (xhr) {
      xhr.open(method, url, true);
      xhr.onreadystatechange = function () { 
          if (xhr.readyState == 4 && xhr.status == 200) {
              setDataIntoNode(idDest, xhr.responseText);
              console.log(xhr.responseText);

              // Después de recibir la respuesta, verifica si el usuario existe
              var estadoExiste = xhr.responseText.includes('Ya existe una inscripción abierta');

              // Obtén una referencia al botón de envío
              var submitButton = document.getElementById('btnInscripciones');

              // Inhabilita el botón si el usuario existe
              submitButton.disabled = estadoExiste;
          } else {
              console.error('Error en la solicitud AJAX:', xhr.status, xhr.statusText);
          }
      }

      xhr.send(formData);
  }
  else {
      console.log('No se pudo instanciar el objeto AJAX!');
  }
}

function conectAjax() {
  /** Retorna el objeto httpRequest que es una insTancia de XMLHttpRequest()
  *   httpRequest se utilizará para enviar peticiones http al servidor
  */
  var httpRequest = false;        		 //	CREA EL OBJETO "AJAX".  
  if (window.XMLHttpRequest) {             // -> Mozilla, Safari, ...
      httpRequest = new XMLHttpRequest();
  } else if (window.ActiveXObject) {       // -> IE
      httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
  }
  return httpRequest;                      // RETORNA el objeto AJAX
}

function setDataIntoNode(idDest, response) {
  var resultDiv = document.getElementById(idDest);
  resultDiv.innerHTML = response;

  // Deshabilitar el botón si el usuario existe
 // Obtén una referencia al botón de envío
  var submitButton = document.getElementById('btnInscripciones');

 // Deshabilita el botón si la respuesta incluye 'Ya existe'
 if (response.includes('Ya existe')) {
     submitButton.disabled = true;
 } else {
     submitButton.disabled = false;
 }
}


function getDataForm(idForm) {
  /**
   * Retorna un objeto FormData() con los name y value de los elementos
   * del formulario cuyo id de formuario es 'idForm' pasado por parámetros.
   * 
   * Preparado para los siguientes type: text, password, checkbox, radio, file y select
   *   
   * https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
   * */
  var formData = new FormData();
  /** Tratamiento para los input, incluye los tipos
   *  tipos: text, password, checkbox, radio, file 
   */
  data = document.forms[idForm].getElementsByTagName("input");                // Obtener los input
  for (let i = 0; i < data.length; i++) {                                        // recorrer los elementos del formulario
      if (data[i].name != undefined && data[i].value != undefined)
          if (data[i].type == 'text' || data[i].type == 'password') {
              formData.append(data[i].name, data[i].value);                 //  agrega a formData el par name/value
          }
          else if ((data[i].type == 'checkbox' || data[i].type == 'radio') && data[i].checked) {
              formData.append(data[i].name, data[i].value);                 //  agrega a formData el par name/value
          }
          else if (data[i].type == 'file') {
              formData.append(data[i].name, data[i].files[0]);              //  agrega a formData el par name/value
          }
  }
  /** Tratamiento para los select 
   *  incluye tanto para una selección simple como para selección múltiple.
   */
  data = document.forms[idForm].getElementsByTagName("select");               // Obtener los select
  for (let i = 0; i < data.length; i++) {                                        // recorrer los elementos del formulario
      if (data[i] != undefined && data[i].type == 'select-one') {                //   Para selección simple
          nombre = data[i].name;                                              //     obtiene el name
          valor = data[i].options[data[i].selectedIndex].value;               //     obtiene el value
          formData.append(nombre, valor);                                   //     agrega a formData el par name/value
      }
      if (data[i] != undefined && data[i].type == 'select-multiple') {            //   Para selección multiple
          nombre = data[i].name;                                              //     obtiene el name
          for (let j = 0; j < data[i].selectedOptions.length; j++) {                //     recorrer los elementos seleccionados
              formData.append(nombre, data[i].selectedOptions[j].value);    //       agrega a formData el par name/value
          }
      }
  }
  return formData;                                                              // retorna el objeto formData
}