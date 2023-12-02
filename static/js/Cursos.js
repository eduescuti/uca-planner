function validarInscripcion() {
    var inscripcion = document.getElementById("inscripcion").value;
    if (inscripcion == 0) {
        document.getElementById("error inscripcion").innerHTML = "*Seleccione una fecha de inscripciones (en caso de no poder seleccionar ninguna, primero debe agregar una inscripcion con estado: 'Abierta')";
    } else {
        document.getElementById("error inscripcion").innerHTML = "";
    }
}

function horasNoEstanSeleccionadas() {

    var horasLunes = document.getElementById("horas-lun").value;
    var horasMartes = document.getElementById("horas-mar").value;
    var horasMiercoles = document.getElementById("horas-mie").value;
    var horasJueves = document.getElementById("horas-jue").value;
    var horasViernes = document.getElementById("horas-vie").value;

    var faltanSeleccionarHoras = (noSelecciona(horasLunes) && noSelecciona(horasMartes)
        && noSelecciona(horasMiercoles) && noSelecciona(horasJueves) && noSelecciona(horasViernes));

    return faltanSeleccionarHoras;
}

function eliminarError() {

    if (horasNoEstanSeleccionadas()) {
        document.getElementById("errorhoras").innerHTML = "*Debe ingresar un rango horario de al menos algún día";
    } else {
        document.getElementById("errorhoras").innerHTML = "";
    }
}

function noSelecciona(campo) {
    return (campo == "")
}

function cupoNoValido(cupo) {
    return (cupo == "" || cupo < 1 || cupo > 100);
}

function indicarQueFaltanCompletarCampos() {
    document.getElementById("errorhoras").innerHTML = "*Debe completar todos los campos";
}

function validarCupo() {
    var cupo = document.getElementById("cupo").value;

    if (cupoNoValido(cupo)) {
        document.getElementById("errorcupo").innerHTML = "*Debe ingresar un cupo válido (MÍNIMO: 1, MÁXIMO: 100)"
    } else {
        document.getElementById("errorcupo").innerHTML = "";
    }
}

function validarDatos() {
    var inscripcion = document.getElementById("inscripcion").value;
    var materia = document.getElementById("mat").value;
    var comision = document.getElementById("comi").value;
    var cupo = document.getElementById("cupo").value;

    if (noSelecciona(inscripcion)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (noSelecciona(materia)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (noSelecciona(comision)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (cupoNoValido(cupo)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (horasNoEstanSeleccionadas()) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else {
        return true;
    }
}