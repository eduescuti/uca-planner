function nombreNoEsValido(nombre) {

    // Expresión regular para permitir solo letras y espacios
    var patron = /^[A-Za-z\s]+$/;

    // Utiliza test() para verificar si el nom cumple con el patrón
    return !patron.test(nombre);
}

function codigoNoValido(codigo) {
    return codigo < 1;
}

function validarNombre() {
    var nombreMateria = document.getElementById("nombre").value;

    if (nombreNoEsValido(nombreMateria)) {
        document.getElementById("error nombre").innerHTML = "*Ingrese un nombre válido";
    } else {
        document.getElementById("error nombre").innerHTML = "";
    }
}

function validarCodigo() {
    var codigo = document.getElementById("codigo").value;

    if (codigoNoValido(codigo)) {
        document.getElementById("error codigo").innerHTML = "*Ingrese un código";
    } else {
        document.getElementById("error codigo").innerHTML = "";
    }
}

function indicarQueFaltanCompletarCampos() {
    document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos";
}

function validarDatos() {

    var nombre = document.getElementById("nombre").value;
    var codigoMateria = document.getElementById("codigo").value;

    if (nombreNoEsValido(nombre)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (codigoNoValido(codigoMateria)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else {
        return true;
    }
}