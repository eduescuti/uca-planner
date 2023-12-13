function resetearCronograma() {
    document.getElementById("materia").value = "";

    for (let dia = 1; dia < 6; dia++) {
        for (let hora = 1; hora < 9; hora++) {
            eliminarMateriasDelCronograma(dia, hora);
        }
    }

}

function eliminarMateriasDelCronograma(dia, hora) {

    var celda = document.getElementById(dia + "-" + hora);

    celda.textContent = "";
    celda.style.background = "white";
}

function validarInscripcion() {
    var inscripcion = document.getElementById("inscripcion").value;
    if (inscripcion == "") {
        document.getElementById("error inscripcion").innerHTML = "*Seleccione una fecha de inscripciones (en caso de no poder seleccionar ninguna, significa que NO hay inscripciones habilitadas para poder inscribirse)";
    } else {
        document.getElementById("error inscripcion").innerHTML = "";
        document.getElementById("materia").disabled = false;
    }
}

function noSelecciona(campo) {
    return (campo == "")
}

function indicarQueFaltanCompletarCampos() {
    document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos para poder inscribirse";
}

function validarDatos() {

    var inscripcion = document.getElementById("inscripcion").value;
    var materia = document.getElementById("materia").value;

    if (noSelecciona(inscripcion)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (noSelecciona(materia)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else {
        return true;
    }
}

function mostrarMateria() {
    var id_com_mat = document.getElementById("materia").value;

    if (id_com_mat != "") {
        listaHorarios = document.getElementsByName(id_com_mat);
        nombreMateria = document.getElementById(id_com_mat).value;

        for (let i = 0; i < listaHorarios.length; i++) {
            var elemento = listaHorarios[i];
            id_dia = elemento.id;
            id_hora = elemento.value;
            var celda = document.getElementById(id_dia + "-" + id_hora);
            celda.innerHTML = nombreMateria;
            celda.style.background = "grey";
            celda.style.color = "white";

        }
    }

}


function verificarCupo(event){


    queryAjaxForm('/inscribirse', 'resCupo', 'formInscripcion')


}


function queryAjaxForm(url, idDest, idForm, method = "POST") {
    var formData = getDataForm(idForm);                     // Obtener los pares 

    var xhr = conectAjax();                               // Creo el objeto AJAX   
    if (xhr) {
        xhr.open(method, url, true);                       // Abré la connección AJAX. false = sincro , true = asincro
        xhr.onreadystatechange = function () {               // CARGA la función en el 'evento' del ajax onreadystatechange
            if (xhr.readyState == 4 && xhr.status == 200) {
                setDataIntoNode(idDest, xhr.responseText) 
                  // CARGAR la respuesta en el html destino
            }
        }
        xhr.send(formData);                                // ENVIA la petición al servidor con los datos de formData (formulario) 
    }
    else {
        console.log('No se pudo instanciar el objeto AJAX!'); // Falló la conección ajax
    }
}

function getDataForm(idForm) {
    var formData = new FormData();

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

function setDataIntoNode(idDest, textHTML) {
//     let oElement; // objeto
//     let sNameTag; // string
//     let elementsReadOnlyInnerHTML;                                 // array donde se almacen los tipos de nodos que no tienen innerHTML
//     elementsReadOnlyInnerHTML = ["INPUT", "COL", "COLGROUP", "FRAMESET", "HEAD", "HTML",
//         "STYLE", "TABLE", "TBODY", "TFOOT", "THEAD", "TITLE", "TR"
//     ];

//     if (document.getElementById(idDest)) {                          // Si existe el 'idDest'
//         oElement = document.getElementById(idDest);                // Obtener el nodo del 'idDest'
//         sNameTag = oElement.tagName.toUpperCase();                 // Pasar a mayuscula el nombre del tag, para luego hacer búsqueda en array
//         //console.log("***"+sNameTag);
//         if (elementsReadOnlyInnerHTML.indexOf(sNameTag) == -1) {    // ¿No está en el array de lo tag que no tienen innerHTML?
//             oElement.innerHTML = textHTML;                         // Asignar el contenido en el nodo de 'idDest' en la ropiedad innerHTML
//         }
//         else if (sNameTag == 'INPUT') {
//             oElement.value = textHTML;                             // Asignar el contenido en la propiedad value
//         }
//         else {
//             setAnyInnerHTML(oElement, textHTML);
//             //console.log('El elemento destino, cuyo id="'+idDest+'", no posee propiedad "innerHTML" ni "value"!');
//         }
//     }
//     else {
//         console.log('El elemento destino, cuyo id="' + idDest + '", no existe!');
//     }
// }



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
}