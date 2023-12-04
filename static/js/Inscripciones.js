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
        document.getElementById("error anio").innerHTML = "*Ingrese un año válido";
    } else {
        document.getElementById("error anio").innerHTML = "";
    }
}

function indicarQueFaltanCompletarCampos() {
    document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos";
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

