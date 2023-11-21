function campoIncompleto(campo) {
    // Asegura que el campo tenga 4 o más caracteres
    // (El campo que se usa por ahora es el del Usuario unicamente)

    if (campo.length < 4) {
        return true;
    }
    return false;
}

function noEsMailValido(mail) {
    // Expresión regular para verificar el formato de un correo electrónico
    var patron = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    // Utiliza test() para verificar si el email cumple con el patrón
    return !patron.test(mail);
}

function noEsContraseniaValida(contrasenia) {
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

function validarMail() {
    var mail = document.getElementById("mail").value;

    if (noEsMailValido(mail)) {
        document.getElementById("error mail").innerHTML = "*Ingrese un mail válido";
    } else {
        document.getElementById("error mail").innerHTML = "";
    }
}

function validarContra() {
    var contra = document.getElementById("contra").value;

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
    // - Valida que el mail sea un mail.
    // - Valida que la contraseña sea mayor que 6 digitos por lo menos.

    var mail = document.getElementById("mail").value;
    var contra = document.getElementById("contra").value;

    if (noEsMailValido(mail)) {
        indicarQueFaltanCompletarCampos();
        return false; // Evitar el envío del formulario

    } else if (noEsContraseniaValida(contra)) {
        indicarQueFaltanCompletarCampos();
        return false; // Evitar el envío del formulario

    } else {
        return true; // Enviar el envío del formulario
    }
}