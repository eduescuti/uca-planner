//Calculo que con la base de datos, tendria estos valores:
//LOS HORARIOS DE LAS MATERIAS

const MATERIAS_LUNES_COM_A = new Map([
    ["repre", [4, 5, 6]],
    ["filo", [9, 10]],
    ["calculoElemental", [11, 12, 13, 14, 15]],
]);

const MATERIAS_MARTES_COM_A = new Map([
    ["repre", [1, 2, 3]]
]);

const MATERIAS_MIERCOLES_COM_A = new Map([
    ["info", [1, 2, 3]],
    ["calculoElemental", [11, 12, 13]],
]);

const MATERIAS_JUEVES_COM_A = new Map([
    ["compl", [1, 2, 3]],
    ["info", [5, 6, 7, 8]],
]);

const MATERIAS_VIERNES_COM_A = new Map([
    ["intro", [1, 2, 3, 4]],
    ["calculoElemental", [11, 12, 13, 14]]
]);

const MATERIAS = new Map([
    ["intro", "Introducción a la Ingeniería"],
    ["filo", "Filosofía"],
    ["calculoElemental", "Cálculo Elemental"],
    ["repre", "Representación Gráfica"],
    ["compl", "Complementos de Matemática"],
    ["info", "Informática General"]
]);

const MATERIAS_COM_A = new Map([
    ["lun", MATERIAS_LUNES_COM_A],
    ["mar", MATERIAS_MARTES_COM_A],
    ["mie", MATERIAS_MIERCOLES_COM_A],
    ["jue", MATERIAS_JUEVES_COM_A],
    ["vie", MATERIAS_VIERNES_COM_A]
]);


const MATERIAS_COM_B = {};

const DIAS = ["lun", "mar", "mie", "jue", "vie"];



function agregarMateria() {
    // Obtiene la materia seleccionada
    var materia = buscarMateriaPorID("materia");

    for (let d of DIAS) { //Por cada dia voy a tener distintos horarios, o hasta NINGUNO...

        var horarios = buscarHorariosDe(materia, d);

        if (noHay(horarios)) {

            for (let hs of horarios) {
                agregarMateriaATabla(materia, d, hs);
            }
        }
    }

}

function buscarMateriaPorID(id) {
    //Busca una materia por ID
    return document.getElementById(id).value;
}

function buscarNombre(materia) {
    //Devuelve el nombre completo de la materia

    return MATERIAS.get(materia);
}

function buscarHorariosDe(materia, dia) {
    //Me deberia dar un array de enteros, que representan los horarios de la materia (del 1 al 15)

    var horarios = MATERIAS_COM_A.get(dia);

    return horarios.get(materia);
}

function noHay(horas) {
    // Devuelve un valor booleano
    // Define si la lista de horarios existe o no

    return (horas != undefined); // es lo mismo que devuelva horas, pero lo pongo asi para que se entienda
}

function agregarMateriaATabla(materia, dia, hora) {
    //Agrega la materia al cronograma de horarios

    var celda = document.getElementById(dia + "-hora-" + hora);

    celda.textContent = buscarNombre(materia);
    celda.style.color = "red"; //Ver como hacer para que sea de varios colores
    celda.style.background = "#a9a9a9"; // Lo mismo
}

function resetearCronograma() {

    for (let d of DIAS) { //Por cada dia voy a tener distintos horarios, o hasta NINGUNO...

        var horarios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];

        for (let hs of horarios) {
            eliminarMateriasDelCronograma(d, hs);
        }
    }
}

function eliminarMateriasDelCronograma(dia, hora) {

    var celda = document.getElementById(dia + "-hora-" + hora);

    celda.textContent = "";
    celda.style.background = "white";
}

function validarInscripcion() {
    var inscripcion = document.getElementById("inscripcion").value;
    if (inscripcion == 0) {
        document.getElementById("error inscripcion").innerHTML = "*Seleccione una fecha de inscripciones (en caso de no poder seleccionar ninguna, significa que NO hay inscripciones habilitadas para poder inscribirse)";
    } else {
        document.getElementById("error inscripcion").innerHTML = "";
        document.getElementById("materia").disabled = false;
    }
}

function validarMateria() {

}

function validarDatos() {
    return true;
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

function ofrecerMaterias(url, idDest, idForm, method = "POST") {

    var formData = getDataForm(idForm);
    /** formData manual
*   Se puede armar los datos name:value de un formulario desde el código
*   JS sin necdidad que existe el forma en el html y así enviar los pares name:value
*   Ej:
*    formData.append('nombre', 'mariano'); // simula ser el name y el valor del input
*    formData.append('apellido', 'diego'); // simula ser el name y el valor del input                                          
*  */
    var xhr = conectAjax();
    if (xhr) {
        xhr.open(method, url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                setDataIntoNode(idDest, xhr.responseText)
            }
        }
        xhr.send(formData);
    }
    else {
        console.log('No se pudo instanciar el objeto AJAX!');
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

function agregarOpcion(idDest, textHTML) {

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

function setAnyInnerHTML(oElement, html) {
    /* agrega el contenido 'html' en undiv hijo de 'oElement' pasado por parámetro*/
    var temp = oElement.ownerDocument.createElement('div');
    //temp.innerHTML = '<table><tbody id="'+tbody.id+'">' + html + '</tbody></table>';
    temp.innerHTML = html;
    oElement.parentNode.replaceChild(temp.firstChild.firstChild, oElement);
}