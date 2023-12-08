function resetearCronograma() {
    document.getElementById("materia").value = "";

    for (let dia = 1; dia < 6; dia++) {
        for (let hora = 1; hora < 9; hora++) {
            eliminarMateriasDelCronograma(dia, hora);
        }
    }

}

function eliminarMateriasDelCronograma(dia, hora) {

    var celda = document.getElementById(dia + "-" + hora);

    celda.textContent = "";
    celda.style.background = "white";
}

function validarInscripcion() {
    var inscripcion = document.getElementById("inscripcion").value;
    if (inscripcion == "") {
        document.getElementById("error inscripcion").innerHTML = "*Seleccione una fecha de inscripciones (en caso de no poder seleccionar ninguna, significa que NO hay inscripciones habilitadas para poder inscribirse)";
    } else {
        document.getElementById("error inscripcion").innerHTML = "";
        document.getElementById("materia").disabled = false;
    }
}

function noSelecciona(campo) {
    return (campo == "")
}

function indicarQueFaltanCompletarCampos() {
    document.getElementById("error incompleto").innerHTML = "*Debe completar todos los campos para poder inscribirse";
}

function validarDatos() {

    var inscripcion = document.getElementById("inscripcion").value;
    var materia = document.getElementById("materia").value;

    if (noSelecciona(inscripcion)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else if (noSelecciona(materia)) {
        indicarQueFaltanCompletarCampos();
        return false;

    } else {
        return true;
    }
}

function mostrarMateria() {
    var id_com_mat = document.getElementById("materia").value;

    if (id_com_mat != "") {
        listaHorarios = document.getElementsByName(id_com_mat);
        nombreMateria = document.getElementById(id_com_mat).value;

        for (let i = 0; i < listaHorarios.length; i++) {
            var elemento = listaHorarios[i];
            id_dia = elemento.id;
            id_hora = elemento.value;
            var celda = document.getElementById(id_dia + "-" + id_hora);
            celda.innerHTML = nombreMateria;
            celda.style.background = "grey";
            celda.style.color = "white";

        }
    }

}