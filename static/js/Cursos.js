function eliminarError(id) {
    var horaElegida = document.getElementById(id).value;

    if (horaElegida > 0) {
        document.getElementById("error horas").innerHTML = "";
    } else {
        document.getElementById("error horas").innerHTML = "*Debe ingresar un rango horario de al menos algún día";
    }
}

function horasNoEstanSeleccionadas() {

    var horasLunes = document.getElementById("horas-lun").value;
    var horasMartes = document.getElementById("horas-mar").value;
    var horasMiercoles = document.getElementById("horas-mie").value;
    var horasJueves = document.getElementById("horas-jue").value;
    var horasViernes = document.getElementById("horas-vie").value;

    var faltanSeleccionarHoras = (horasLunes == "0" && horasMartes == "0"
        && horasMiercoles == "0" && horasJueves == "0" && horasViernes == "0");

    return faltanSeleccionarHoras;
}

function indicarQueFaltanCompletarCampos() {
    document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos";
}

function cupoNoValido(cupo) {
    return (cupo == "" || cupo < 1 || cupo > 100);
}

function validarCupo() {
    var cupo = document.getElementById("cupo").value;

    if (cupoNoValido(cupo)) {
        document.getElementById("error cupo").innerHTML = "*Debe ingresar un cupo válido (MÍNIMO: 1, MÁXIMO: 100)"
    } else {
        document.getElementById("error cupo").innerHTML = "";
    }
}

function validarDatos() {
    var cupo = document.getElementById("cupo").value;

    if (horasNoEstanSeleccionadas()) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (cupoNoValido(cupo)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else {
        return true;
    }
}