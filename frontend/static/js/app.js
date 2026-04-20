/* ============================================================================
   HERRADURA — Global JS
   Handles the mobile sidebar, toast auto-dismiss, progressive-enhancement of
   Django's default text inputs into date/datetime pickers, and a
   confirm-before-action hook for destructive links.
   ========================================================================= */
(function () {
    'use strict';

    // ---- Sidebar toggle (mobile) -----------------------------------------
    const burger = document.querySelector('[data-sidebar-toggle]');
    const sidebar = document.querySelector('.sidebar');
    if (burger && sidebar) {
        burger.addEventListener('click', function () {
            sidebar.classList.toggle('is-open');
        });
        document.addEventListener('click', function (e) {
            if (!sidebar.contains(e.target) && !burger.contains(e.target)) {
                sidebar.classList.remove('is-open');
            }
        });
    }

    // ---- Toast auto-dismiss ----------------------------------------------
    document.querySelectorAll('.toast').forEach(function (t) {
        setTimeout(function () {
            t.style.transition = 'opacity .4s, transform .4s';
            t.style.opacity = '0';
            t.style.transform = 'translateX(30px)';
            setTimeout(function () { t.remove(); }, 400);
        }, 4500);
        t.addEventListener('click', function () { t.remove(); });
    });

    // ---- Helper: nicer datetime-local inputs ------------------------------
    // Django renders DateTimeField as <input type="text"> by default. If the
    // backend updates to DateTimeInput(attrs={'type':'datetime-local'}) this
    // will just work, but meanwhile we upgrade text fields named start_time /
    // end_time on the client for a better UX.
    document.querySelectorAll('.form input[name="start_time"], .form input[name="end_time"]').forEach(function (el) {
        if (el.type === 'text') el.type = 'datetime-local';
    });
    document.querySelectorAll('.form input[name="date_of_birth"], .form input[name="date"], .form input[name="next_due_date"], .form input[name="start_date"], .form input[name="end_date"], .form input[name="due_date"]').forEach(function (el) {
        if (el.type === 'text') el.type = 'date';
    });

    // ---- Confirm-before-delete hook --------------------------------------
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(el.getAttribute('data-confirm'))) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    });
})();
