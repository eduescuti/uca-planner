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
    document.getElementById("error_anio").innerHTML = "*Ingrese un año válido";
  } else {
    document.getElementById("error_anio").innerHTML = "";
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
  var filtro = document.getElementById('inputFiltro').value.toLowerCase();
  console.log(filtro)
  var filas = document.getElementById('tablaCurso').getElementsByTagName('tbody')[0].getElementsByTagName('tr');

  for (var i = 0; i < filas.length; i++) {
    var fila = filas[i];
    var celdas = fila.getElementsByTagName('td');
    var coincide = false;

    for (var j = 0; j < celdas.length; j++) {
      var dato = celdas[j];
      if (dato.textContent.toLowerCase().includes(filtro)) {
        coincide = true;
        break;
      }
    }

    fila.style.display = coincide ? '' : 'none';
  }
}

//coincide ? '' : 'none'    coincide ? (true) : (false)
// si es true sera una cadena vacia si es false sera none 


function validarEstado(){
  var selectEstado = document.getElementById('estado');
  var option = selectEstado.value.trim(); // Obtiene el valor seleccionado en el select
  var boton = document.getElementById('btnInscripciones');


  queryAjaxForm('/validar_estado/' + option , 'resAjax', 'formInscripciones')
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


function sortDesplegables(){
     // Obtener el contenedor de inscripciones
     var inscripcionesContainer = document.querySelector('.inscripciones');

     // Obtener todos los elementos <details> con la clase "prueba" dentro del contenedor
     var detailsList = inscripcionesContainer.querySelectorAll('details.prueba');
 
     // Convertir la NodeList a un array
     var detailsArray = Array.from(detailsList);
 
     // Ordenar los elementos <details> en función de los textos de los elementos <summary>
     detailsArray.sort(function (a, b) {
         var textA = a.querySelector('summary').textContent;
         var textB = b.querySelector('summary').textContent;
         return textA.localeCompare(textB);
     });
 
     // Mover cada elemento <details> ordenado al final del contenedor
     detailsArray.forEach(function (details) {
         inscripcionesContainer.appendChild(details);
     });
 }




function cerrarIns() {
  var idInscripcion = document.getElementById('btnCierre').getAttribute('idIns');

  console.log(idInscripcion)
  queryAjaxFormCierre('/cerrar_inscripcion/'+ idInscripcion,'resCierre', 'formCierre' + idInscripcion)

}

function queryAjaxFormCierre(url, idDest, idForm, method = "POST") {
  var formData = getDataForm(idForm);                     // Obtener los pares 

  var xhr = conectAjax();                               // Creo el objeto AJAX   
  if (xhr) {
      xhr.open(method, url, true);                       // Abré la connección AJAX. false = sincro , true = asincro
      xhr.onreadystatechange = function () {               // CARGA la función en el 'evento' del ajax onreadystatechange
          if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.responseText)
            setDataIntoNodeCierre(idDest, xhr.responseText)   // CARGAR la respuesta en el html destino
            
        }
    };
      xhr.send(formData);                                // ENVIA la petición al servidor con los datos de formData (formulario) 
  }
  else {
      console.log('No se pudo instanciar el objeto AJAX!'); // Falló la conección ajax
  }

function setDataIntoNodeCierre(idDest, textHTML) {
  let oElement; // objeto
  let sNameTag; // string
  let elementsReadOnlyInnerHTML;                                 // array donde se almacen los tipos de nodos que no tienen innerHTML
  elementsReadOnlyInnerHTML = ["INPUT", "COL", "COLGROUP", "FRAMESET", "HEAD", "HTML",
      "STYLE", "TABLE", "TBODY", "TFOOT", "THEAD", "TITLE", "TR"
  ];

  if (document.getElementById(idDest)) {                          // Si existe el 'idDest'
      oElement = document.getElementById(idDest);                // Obtener el nodo del 'idDest'
      sNameTag = oElement.tagName.toUpperCase();                 // Pasar a mayuscula el nombre del tag, para luego hacer búsqueda en array
      //console.log("***"+sNameTag);
      if (elementsReadOnlyInnerHTML.indexOf(sNameTag) == -1) {    // ¿No está en el array de lo tag que no tienen innerHTML?
          oElement.innerHTML = textHTML;                         // Asignar el contenido en el nodo de 'idDest' en la ropiedad innerHTML
      }
      else if (sNameTag == 'INPUT') {
          oElement.value = textHTML;                             // Asignar el contenido en la propiedad value
      }
      else {
          setAnyInnerHTML(oElement, textHTML);
          //console.log('El elemento destino, cuyo id="'+idDest+'", no posee propiedad "innerHTML" ni "value"!');
      }
  }
  else {
      console.log('El elemento destino, cuyo id="' + idDest + '", no existe!');
  }
}

}

