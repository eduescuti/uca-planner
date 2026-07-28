/* ============================================================
   UCA Planner · Utilidades de las pantallas de autenticación
   Mejora progresiva: si este script no carga, los formularios
   siguen funcionando exactamente igual.
   ============================================================ */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        var toggles = document.querySelectorAll(".pw-toggle");

        Array.prototype.forEach.call(toggles, function (btn) {
            var input = document.getElementById(btn.getAttribute("data-target"));
            if (!input) return;

            btn.addEventListener("click", function () {
                var oculta = input.type === "password";
                input.type = oculta ? "text" : "password";
                btn.setAttribute("aria-pressed", oculta ? "true" : "false");
                btn.setAttribute(
                    "aria-label",
                    oculta ? "Ocultar contraseña" : "Mostrar contraseña"
                );
                input.focus();
            });
        });
    });
})();
