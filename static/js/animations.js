/* ============================================================
   UCA Planner · Micro-interacciones con Motion (motion.dev)
   Mejora progresiva: si Motion no está disponible, la página
   igual se ve bien gracias a las animaciones CSS de theme.css.
   No modifica ninguna funcionalidad existente.
   ============================================================ */
(function () {
    "use strict";

    var reduced = window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;

    // Motion (build UMD) expone el objeto global `Motion`.
    var M = window.Motion;
    if (!M || typeof M.animate !== "function") return;

    var animate = M.animate;
    var inView = M.inView;
    var stagger = M.stagger;

    var springSoft = { type: "spring", stiffness: 320, damping: 22 };
    var springSnap = { type: "spring", stiffness: 520, damping: 18 };

    function all(sel, root) {
        return Array.prototype.slice.call((root || document).querySelectorAll(sel));
    }

    document.addEventListener("DOMContentLoaded", function () {

        /* ---- 1. Reveal al entrar en viewport (tarjetas, filas, paneles) ---- */
        var revealables = all(
            ".card, .panel, .contenedor, #contenedor, details.prueba, .tabla, .titulo"
        );
        revealables.forEach(function (el) {
            el.style.opacity = "0";
            el.style.transform = "translateY(26px)";
        });

        if (typeof inView === "function") {
            revealables.forEach(function (el) {
                inView(el, function () {
                    animate(
                        el,
                        { opacity: [0, 1], y: [26, 0] },
                        { duration: 0.6, easing: [0.22, 1, 0.36, 1] }
                    );
                    return function () {}; // no repetir al salir
                }, { amount: 0.15 });
            });
        } else {
            revealables.forEach(function (el) {
                el.style.opacity = "";
                el.style.transform = "";
            });
        }

        /* ---- 2. Entrada escalonada de filas de tablas de horarios ---- */
        var rows = all("#cronograma tbody tr, .tabla tbody tr");
        if (rows.length && typeof stagger === "function") {
            animate(
                rows,
                { opacity: [0, 1], transform: ["translateX(-14px)", "translateX(0px)"] },
                { delay: stagger(0.04), duration: 0.5, easing: [0.22, 1, 0.36, 1] }
            );
        }

        /* ---- 3. Física de resorte al pasar el mouse / presionar ---- */
        var interactive = all(
            ".boton, .cta, input[type=submit], input[type=button], button, " +
            "#btnInscripciones, #btnOrden, #btnAgregarCurso, #volver, " +
            ".cierre-ins, .agr-curso"
        );
        interactive.forEach(function (el) {
            el.addEventListener("pointerenter", function () {
                animate(el, { scale: 1.05 }, springSoft);
            });
            el.addEventListener("pointerleave", function () {
                animate(el, { scale: 1 }, springSoft);
            });
            el.addEventListener("pointerdown", function () {
                animate(el, { scale: 0.94 }, springSnap);
            });
            el.addEventListener("pointerup", function () {
                animate(el, { scale: 1.05 }, springSnap);
            });
        });

        /* ---- 4. Tarjetas ---- */
        // ¿Estamos en el home? (tiene la imagen del campus dentro de .row)
        var isHome = !!document.querySelector(".row .imagen");
        var homeCards = isHome ? all(".row .card") : [];

        // 4a. Cards genéricas (no-home): elevación simple con resorte.
        all(".card").forEach(function (el) {
            if (homeCards.indexOf(el) !== -1) return;
            el.addEventListener("pointerenter", function () {
                animate(el, { scale: 1.02 }, springSoft);
            });
            el.addEventListener("pointerleave", function () {
                animate(el, { scale: 1 }, springSoft);
            });
        });

        // 4b. Cards del home: inclinación 3D que sigue al cursor + spotlight.
        homeCards.forEach(function (card) {
            card.addEventListener("pointermove", function (e) {
                var r = card.getBoundingClientRect();
                var px = (e.clientX - r.left) / r.width;   // 0..1
                var py = (e.clientY - r.top) / r.height;    // 0..1
                card.style.setProperty("--mx", (px * 100) + "%");
                card.style.setProperty("--my", (py * 100) + "%");
                animate(card, {
                    rotateX: (0.5 - py) * 9,
                    rotateY: (px - 0.5) * 12,
                    scale: 1.035
                }, { duration: 0.3, easing: [0.22, 1, 0.36, 1] });
            });
            card.addEventListener("pointerleave", function () {
                animate(card, { rotateX: 0, rotateY: 0, scale: 1 }, springSoft);
            });
        });

        /* ---- 5. Enlaces de navegación: sutil salto ---- */
        all(".topnav a").forEach(function (el) {
            el.addEventListener("pointerenter", function () {
                animate(el, { y: -2 }, springSnap);
            });
            el.addEventListener("pointerleave", function () {
                animate(el, { y: 0 }, springSnap);
            });
        });
    });
})();
