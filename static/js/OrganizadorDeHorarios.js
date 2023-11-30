//Calculo que con la base de datos, tendria estos valores:
//LOS HORARIOS DE LAS MATERIAS

const MATERIAS_LUNES_COM_A = new Map([
    ["repre", [4, 5, 6]],
    ["filo", [9, 10]],
    ["calculoElemental", [11, 12, 13, 14, 15]],
]);

const MATERIAS_MARTES_COM_A = new Map([
    ["repre", [1, 2, 3]]
]);

const MATERIAS_MIERCOLES_COM_A = new Map([
    ["info", [1, 2, 3]],
    ["calculoElemental", [11, 12, 13]],
]);

const MATERIAS_JUEVES_COM_A = new Map([
    ["compl", [1, 2, 3]],
    ["info", [5, 6, 7, 8]],
]);

const MATERIAS_VIERNES_COM_A = new Map([
    ["intro", [1, 2, 3, 4]],
    ["calculoElemental", [11, 12, 13, 14]]
]);

const MATERIAS = new Map([
    ["intro", "Introducción a la Ingeniería"],
    ["filo", "Filosofía"],
    ["calculoElemental", "Cálculo Elemental"],
    ["repre", "Representación Gráfica"],
    ["compl", "Complementos de Matemática"],
    ["info", "Informática General"]
]);

const MATERIAS_COM_A = new Map([
    ["lun", MATERIAS_LUNES_COM_A],
    ["mar", MATERIAS_MARTES_COM_A],
    ["mie", MATERIAS_MIERCOLES_COM_A],
    ["jue", MATERIAS_JUEVES_COM_A],
    ["vie", MATERIAS_VIERNES_COM_A]
]);


const MATERIAS_COM_B = {};

const DIAS = ["lun", "mar", "mie", "jue", "vie"];



function agregarMateria() {
    // Obtiene la materia seleccionada
    var materia = buscarMateriaPorID("materia");

    for (let d of DIAS) { //Por cada dia voy a tener distintos horarios, o hasta NINGUNO...

        var horarios = buscarHorariosDe(materia, d);

        if (noHay(horarios)) {

            for (let hs of horarios) {
                agregarMateriaATabla(materia, d, hs);
            }
        }
    }

}

function buscarMateriaPorID(id) {
    //Busca una materia por ID
    return document.getElementById(id).value;
}

function buscarNombre(materia) {
    //Devuelve el nombre completo de la materia

    return MATERIAS.get(materia);
}

function buscarHorariosDe(materia, dia) {
    //Me deberia dar un array de enteros, que representan los horarios de la materia (del 1 al 15)

    var horarios = MATERIAS_COM_A.get(dia);

    return horarios.get(materia);
}

function noHay(horas) {
    // Devuelve un valor booleano
    // Define si la lista de horarios existe o no

    return (horas != undefined); // es lo mismo que devuelva horas, pero lo pongo asi para que se entienda
}

function agregarMateriaATabla(materia, dia, hora) {
    //Agrega la materia al cronograma de horarios

    var celda = document.getElementById(dia + "-hora-" + hora);

    celda.textContent = buscarNombre(materia);
    celda.style.color = "red"; //Ver como hacer para que sea de varios colores
    celda.style.background = "#a9a9a9"; // Lo mismo
}

function resetearCronograma() {

    for (let d of DIAS) { //Por cada dia voy a tener distintos horarios, o hasta NINGUNO...

        var horarios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];

        for (let hs of horarios) {
            eliminarMateriasDelCronograma(d, hs);
        }
    }
}

function eliminarMateriasDelCronograma(dia, hora) {

    var celda = document.getElementById(dia + "-hora-" + hora);

    celda.textContent = "";
    celda.style.background = "white";
}

function validarInscripcion() {
    var inscripcion = document.getElementById("inscripcion").value;
    if (inscripcion == 0) {
        document.getElementById("error inscripcion").innerHTML = "*Seleccione una fecha de inscripciones (en caso de no poder seleccionar ninguna, significa que NO hay inscripciones habilitadas para poder inscribirse)";
    } else {
        document.getElementById("error inscripcion").innerHTML = "";
    }
}

function validarDatos() {
    return true;
}