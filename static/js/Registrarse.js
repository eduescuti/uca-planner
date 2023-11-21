
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