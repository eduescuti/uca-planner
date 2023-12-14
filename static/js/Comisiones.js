function comisionNoValida(comision) {
    var cantidadDeLetras = comision.length;

    return (noEsValido(comision) || cantidadDeLetras > 2);
}

function anioNoValido(anio) {
    return anio < (obtenerAnioActual());
}

function cuatrimestreNoValido(cuatri) {
    return cuatri == "0";
}

function noEsValido(nom) {
    // Expresión regular para permitir solo letras y espacios
    var patron = /^[A-Za-z\s]+$/;

    // Utiliza test() para verificar si el nom cumple con el patrón
    return !patron.test(nom);
}

function validarNombre() {
    var nombreComision = document.getElementById("comision").value;

    if (comisionNoValida(nombreComision)) {
        document.getElementById("error comision").innerHTML = "*Ingrese un nombre válido (deben ser únicamente dos letras)";
    } else {
        document.getElementById("error comision").innerHTML = "";
    }
}

function indicarQueFaltanCompletarCampos() {
    document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos";
}

function validarDatos() {
    var nombreComision = document.getElementById("comision").value;

    if (comisionNoValida(nombreComision)) {
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

function validar_comision() {
    var inputComision = document.getElementById('comision');
    var comision = inputComision.value.trim(); // Toma el valor del input

    queryAjaxForm('/validar_comision/' + comision, 'resComision', 'formComision');

}

function queryAjaxForm(url, idDest, idForm, method = "POST") {
    var formData = getDataForm(idForm);
    var xhr = conectAjax();

    if (xhr) {
        xhr.open(method, url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                setDataIntoNode(idDest, xhr.responseText);

                // Después de recibir la respuesta, verifica si existe
                var nombreExiste = xhr.responseText.includes('El nombre de la comision ya existe.');

                // Referencia al botón de envío
                var submitButton = document.getElementById('btnSubmit');

                // Inhabilita el botón si al menos una de las cadenas existe
                submitButton.disabled = nombreExiste

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

    var submitButton = document.getElementById('btnSubmit');

    // Deshabilitar el botón si el usuario existe
    if (response.includes('ya existe')) {
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