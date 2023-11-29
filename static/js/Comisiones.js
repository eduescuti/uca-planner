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