
function campoIncompleto(campo) {
    // Asegura que el campo tenga 4 o más caracteres
    // (El campo que se usa por ahora es el del Usuario unicamente)

    if (campo.length < 4) {
        return true;
    }
    return false;
}

function rolIncompleto() {
    // Asegura que se haya seleccionado alguna de las Sedes de la UCA

    var rolAlumno = document.getElementById("rolAlumno");
    var rolAdmin = document.getElementById("rolAdmin");

    var completoElRol = (rolAlumno.checked || rolAdmin.checked);

    if (completoElRol) {
        return false;
    }
    return true;

}

function noEsValido(nom) {
    // Expresión regular para permitir solo letras y espacios
    var patron = /^[A-Za-z\s]+$/;

    // Utiliza test() para verificar si el nom cumple con el patrón
    return !patron.test(nom);
}

function noEsMailValido(mail) {
    // Expresión regular para verificar el formato de un correo electrónico
    var patron = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    // Utiliza test() para verificar si el email cumple con el patrón
    return !patron.test(mail);
}

function noEsContraseniaValida(contrasenia) {
    // Asegura que la contraseña tenga por lo menos más de 6 caracteres

    let x = contrasenia.length;
    if (x < 6) {
        return true;
    }
    return false;
}

function validarUsuario() {
    var usuario = document.getElementById("usuario").value;

    if (campoIncompleto(usuario)) {
        document.getElementById("error usuario").innerHTML = "*Ingrese un nombre de usuario de 4 o más caracteres";
    } else {
        document.getElementById("error usuario").innerHTML = "";
    }
}

function validarNombre() {
    var nombre = document.getElementById("nombre").value;

    if (noEsValido(nombre)) {
        document.getElementById("error nombre").innerHTML = "*Ingrese un nombre válido";
    } else {
        document.getElementById("error nombre").innerHTML = "";
    }
}

function validarApellido() {
    var apellido = document.getElementById("apellido").value;

    if (noEsValido(apellido)) {
        document.getElementById("error apellido").innerHTML = "*Ingrese un apellido válido";
    } else {
        document.getElementById("error apellido").innerHTML = "";
    }
}

function validarMail() {
    var mail = document.getElementById("email").value;

    if (noEsMailValido(mail)) {
        document.getElementById("error email").innerHTML = "*Ingrese un mail válido";
    } else {
        document.getElementById("error email").innerHTML = "";
    }
}

function validarContra() {
    var contra = document.getElementById("contraseña").value;

    if (noEsContraseniaValida(contra)) {
        document.getElementById("error contra").innerHTML = "*La contraseña debe tener al menos 6 caracteres";
    } else {
        document.getElementById("error contra").innerHTML = "";
    }
}

function indicarQueFaltanCompletarCampos() {
    document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos";
}

function validarDatos() {
    // - Valida que el usuario sea un string con por lo menos 4 caracteres.
    // - Valida que el nombre, apellido no tengan numeros ni sea un espacio en blanco.
    // - Valida que el mail sea un mail.
    // - Valida que la contraseña sea mayor que 6 digitos por lo menos.
    // - Valida que la carrera del usuario y la sede, estén seleccionadas.

    var usuario = document.getElementById("usuario").value;
    var nombre = document.getElementById("nombre").value;
    var apellido = document.getElementById("apellido").value;
    var mail = document.getElementById("email").value;
    var contra = document.getElementById("contraseña").value;

    if (campoIncompleto(usuario)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (noEsValido(nombre)) {
        indicarQueFaltanCompletarCampos();
        return false; // Evitar el envío del formulario

    } else if (noEsValido(apellido)) {
        indicarQueFaltanCompletarCampos();
        return false; // Evitar el envío del formulario

    } else if (noEsMailValido(mail)) {
        indicarQueFaltanCompletarCampos();
        return false; // Evitar el envío del formulario

    } else if (noEsContraseniaValida(contra)) {
        indicarQueFaltanCompletarCampos();
        return false; // Evitar el envío del formulario

    } else if (rolIncompleto()) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else {
        return true; // Enviar el envío del formulario
    }
}


// function validateOnKeyUp() {
//     const inputUsuario = $('#usuario');
//     const username = inputUsuario.val(); //toma el valor del input
//     const resultDiv = $('#respuesta');
//     const submitButton = $('#btnSubmmit');


//     // Realizar la solicitud AJAX con jQuery
//     $.ajax({
//         url: '/validate-username/${username}',  // url donde realiza la peticion, incluye el nombre del usuario
//         method: 'GET', //método http que utiliza
//         dataType: 'json', // espera respuesta de tipo json
//         success: function (data) { 
//             const resultDiv = $('#respuesta');
                
//                 if (data.exists) {       // data es el parámetro que tiene la respuesta json; exist indica si existe o no en la BD
//                     resultDiv.html('El nombre de usuario ya existe.');

//                     // Deshabilitar el botón de envío si el usuario existe
//                     submitButton.prop('disabled', true);
//                 } else {
//                     resultDiv.html('El nombre de usuario está disponible.');
//                     // Habilitar el botón de envío si el usuario no existe
//                     submitButton.prop('disabled', false);
//                 }
//             },
//             error: function (error) {
//                 console.error('Error:', error);
//             }
//         });
    



function validarUsuario() {
    var inputUsuario = document.getElementById('usuario');
    var username = inputUsuario.value.trim(); // Toma el valor del input
    var submitButton = document.getElementById('btnSubmit');
    
    queryAjaxForm('/validar_usuario/' + username, 'respuesta', 'formRegistro');
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
                    var userExists = xhr.responseText.includes('El nombre de usuario ya existe.');

                    // Obtén una referencia al botón de envío
                    var submitButton = document.getElementById('btnSubmit');

                    // Inhabilita el botón si el usuario existe
                    submitButton.disabled = userExists;
                } else {
                    console.error('Error en la solicitud AJAX:', xhr.status, xhr.statusText);
                }
            }
        
        xhr.send(formData);
    } 
    else {
        console.log('No se pudo instanciar el objeto AJAX!');
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
}