/** Estados de la petición http
 *  
 * Ready State:
 *   0: La peticion no se ha inicializado
 *   1: Conexion con el servidor establecida
 *   2: Peticion recibida
 *   3: Procesando Peticion
 *   4: Peticion finalizada y la respuesta esta lista.
 *
 * Status:
 *   200: ok
 *   404: Pagina no encontrada
 * 
 * https://developer.mozilla.org/es/docs/Web/Guide/AJAX/Getting_Started
 * http://www.saregune.net/ikasi/hezigune/curso.php?curso=ajax&leccion=ajax_xml_intro
 * 
*/

// ======= + + + + + INICIO: FUNCIONES AJAX + + + + + =========
// ==== XMLHttpRequest es el objeto "AJAX"
// ======= + + + + + + + + + + + + + + + + + + + + + =========
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

function queryAjax(url, idDest, method = "POST") {
    /**
        * Realiza una una petición request al servidor 'url'. NO envía datos 
        * al servidor 'xhr.send(null)', sólo hace la petición a la url y 
        * almacena la respuesta dentro del nodo cuyo id sea 'idDest'
        * 
        * url:    es la dirección donde se obtiene los datos (el servidor)
        * idDest: es el id de un elemento html donde se escribirán los datos recibido de la url
        * method: es el metodo del request, puede ser POST o GET. Por defaul es POST
        */
    var xhr = conectAjax();                                     // Creo el objeto AJAX     
    if (xhr) {
        xhr.open(method, url, true);                              // Abre la connección AJAX. false = sincro , true = asincro
        xhr.onreadystatechange = function () {                     // CARGA la función en el 'evento' del ajax onreadystatechange
            if (xhr.readyState != 1) {
                document.body.style.cursor = 'wait';                 // Setea la espera: Poner el cursor del mouse en espera
                /* Otra opción sería: agregar una imagen de espera en el div 
                     (o elemento) donde serán cargado los datos y así liberar 
                     el puntero del mouse */
            }
            if (xhr.readyState == 4 && xhr.status == 200) {
                document.body.style.cursor = 'default';        // Resetea la espera: Poner el cursor del mouse en normal
                textHTML = xhr.responseText;                   // RECUPERA la respuesta que viene del servidor en formato html
                setDataIntoNode(idDest, textHTML);              // CARGAR la respuesta en el html destino
            }
        }
        xhr.send(null);
    }
    else {
        console.log('No se pudo instanciar el objeto AJAX!'); // Falló la conección
    }
}

function queryAjaxForm(url, idDest, idForm, method = "POST") {
    /**
     * Realiza una una petición request al servidor 'url'. ENVIA datos 
     * de un formulario al servidor 'xhr.send(formData)'; es decir envia pares 
     * name : value (por post o por get) del formulario cuyo id es 'idForm'. 
     * Almacena la respuesta dentro del nodo cuyo id es 'idDest'
     * 
     * url:    es la dirección donde se obtiene los datos (el servidor)
     * idDest: es el id de un elemento html donde se escribirán los datos recibido de la url
     * idForm: es el id del formulario del cual se enviarán lo pares claves / valor.
     * method: es el metodo del request, puede ser POST o GET. Por defaul es POST
     * 
     * https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_forms_through_JavaScript
     * */

    var formData = getDataForm(idForm);                     // Obtener los pares 
    /** formData manual
*  Se puede armar los datos name:value de un formulario desde el código
*  JS sin necdidad que existe el forma en el html y así enviar los pares name:value
*  Ej:
*    formData.append('nombre', 'mariano'); // simula ser el name y el valor del input
*    formData.append('apellido', 'diego'); // simula ser el name y el valor del input                                          
*  */
    var xhr = conectAjax();                               // Creo el objeto AJAX   
    if (xhr) {
        xhr.open(method, url, true);                       // Abré la connección AJAX. false = sincro , true = asincro
        xhr.onreadystatechange = function () {               // CARGA la función en el 'evento' del ajax onreadystatechange
            if (xhr.readyState == 4 && xhr.status == 200) {
                setDataIntoNode(idDest, xhr.responseText)   // CARGAR la respuesta en el html destino
            }
        }
        xhr.send(formData);                                // ENVIA la petición al servidor con los datos de formData (formulario) 
    }
    else {
        console.log('No se pudo instanciar el objeto AJAX!'); // Falló la conección ajax
    }
}
/* =========- - - - - - FIN: FUNCIONES AJAX - - - - - - =======*/

/* ============+ + + + INICIO: FUNCIONES AUXILIARES + + +======
// ============================================================
// ==== Funciones Auxiliares que NO SON AJAX pero las utilizamos
// ==== para cumplir los objetivos
// ============================================================*/

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

function setDataIntoNode(idDest, textHTML) {
    /**
     * Realiza la carga de un html 'textHTML' en el nodo cuyo id es 'idDest'
     * 
     * 'textHTML' es un texto en formato html 
     * 'idDes' es un id de un tag html dentro del documento y es donde se cargará
     *         el contenido de 'textHTML'
     * 
     * Comentario: Esta función se realiza debido a que hay distintos tratamientos
     *              para asignar contenido html a un nodo.
     * 
     * Conlclusión: Lo mejor (en la medida que se pueda) designar un 'idDest' de un tag 'div' 
     *              para colocar la información 'textHTML'. Esto es mejor porque div 
     *              tiene la propiedad innerHTML.
     *              
     */

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
/* ============- - - -  INICIO: FUNCIONES AUXILIARES - - - ====== */


function verificar_datos(url, idDest, idForm, method = "POST") {

    var formData = getDataForm(idForm);                     // Obtener los pares 

    var xhr = conectAjax();                               // Creo el objeto AJAX   
    if (xhr) {
        xhr.open(method, url, true);                       // Abré la connección AJAX. false = sincro , true = asincro
        xhr.onreadystatechange = function () {               // CARGA la función en el 'evento' del ajax onreadystatechange
            if (xhr.readyState == 4 && xhr.status == 200) {
                setDataIntoNode(idDest, xhr.responseText)   // CARGAR la respuesta en el html destino
            }
        }
        xhr.send(formData);                                // ENVIA la petición al servidor con los datos de formData (formulario) 
    }
    else {
        console.log('No se pudo instanciar el objeto AJAX!'); // Falló la conección ajax
    }
}