/* ============================================================================
   Dashboard charts
   ----------------------------------------------------------------------------
   Each chart below only initialises if its corresponding <canvas> exists in
   the DOM, so this single script supports all three role-specific dashboards
   without role-checks here. Data comes from data-* attributes the Django
   template renders from real backend context — no hardcoded fallbacks.

   Bootstrapping is defensive: the script waits for DOMContentLoaded, then
   retries briefly if Chart.js hasn't yet finished loading (rare but it
   happens when the CDN is slow or a browser extension delays it). If
   Chart.js is genuinely missing, we log one clear console message instead
   of silently failing — which was the previous behaviour, making
   "no chart" debugging almost impossible.
   ========================================================================= */
(function () {
    'use strict';

    function bootstrap() {
        if (typeof Chart !== 'undefined') {
            initCharts();
            return;
        }
        // Chart.js may still be loading — retry up to ~2s
        let attempts = 0;
        const retry = setInterval(function () {
            attempts += 1;
            if (typeof Chart !== 'undefined') {
                clearInterval(retry);
                initCharts();
            } else if (attempts > 20) {
                clearInterval(retry);
                console.warn(
                    '[dashboard] Chart.js never became available. ' +
                    'The CDN script at cdn.jsdelivr.net may be blocked or slow. ' +
                    'Charts will not render on this page.'
                );
            }
        }, 100);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootstrap);
    } else {
        bootstrap();
    }

    function initCharts() {
    'use strict';

    Chart.defaults.font.family = "'Geist', 'Manrope', -apple-system, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = '#7a7569';
    Chart.defaults.borderColor = 'rgba(230, 223, 206, 0.8)';

    const BRAND = {
        primary: '#1f3a2a',
        primaryFade: 'rgba(31, 58, 42, 0.12)',
        accent:  '#b8893a',
        accentFade: 'rgba(184, 137, 58, 0.18)',
        ink:     '#181c18',
        muted:   '#7a7569',
        success: '#2f6d47',
        danger:  '#9a3b2f',
        warning: '#b87a17',
    };

    const palette = [
        BRAND.primary, BRAND.accent, '#5a7a4a', '#c5a572',
        '#3b5a45', '#a0763a', '#7a8c6d', '#d4b78c',
    ];

    function readAttr(canvas, name, fallback) {
        const raw = canvas.dataset[name];
        if (!raw) return fallback;
        try { return JSON.parse(raw); } catch (e) { return fallback; }
    }

    // ─── Admin: monthly revenue (bar) ────────────────────────────────────
    const revC = document.getElementById('chart-revenue-monthly');
    if (revC) {
        new Chart(revC, {
            type: 'bar',
            data: {
                labels: readAttr(revC, 'labels', []),
                datasets: [{
                    label: 'Revenue (€)',
                    data:  readAttr(revC, 'values', []),
                    backgroundColor: BRAND.primary,
                    borderRadius: 6,
                    borderSkipped: false,
                    barThickness: 32,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: BRAND.ink,
                        callbacks: { label: c => '€ ' + c.parsed.y.toLocaleString() },
                    },
                },
                scales: {
                    y: { beginAtZero: true, ticks: { callback: v => '€' + v }, grid: { color: 'rgba(230,223,206,.5)' } },
                    x: { grid: { display: false } },
                },
            },
        });
    }

    // ─── Admin: monthly memberships (bar) ────────────────────────────────
    const memC = document.getElementById('chart-memberships-monthly');
    if (memC) {
        new Chart(memC, {
            type: 'bar',
            data: {
                labels: readAttr(memC, 'labels', []),
                datasets: [{
                    label: 'New memberships',
                    data:  readAttr(memC, 'values', []),
                    backgroundColor: BRAND.accent,
                    borderRadius: 6,
                    borderSkipped: false,
                    barThickness: 32,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { backgroundColor: BRAND.ink } },
                scales: {
                    y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: 'rgba(230,223,206,.5)' } },
                    x: { grid: { display: false } },
                },
            },
        });
    }

    // ─── Admin: horse workload (doughnut) ────────────────────────────────
    const workC = document.getElementById('chart-horse-workload');
    if (workC) {
        new Chart(workC, {
            type: 'doughnut',
            data: {
                labels: readAttr(workC, 'labels', []),
                datasets: [{
                    data: readAttr(workC, 'values', []),
                    backgroundColor: palette,
                    borderWidth: 0,
                    hoverOffset: 6,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false, cutout: '60%',
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 10, padding: 12, font: { size: 11 } } },
                    tooltip: { backgroundColor: BRAND.ink },
                },
            },
        });
    }

    // ─── Member: monthly riding activity (bar) ───────────────────────────
    const actC = document.getElementById('chart-my-activity');
    if (actC) {
        new Chart(actC, {
            type: 'bar',
            data: {
                labels: readAttr(actC, 'labels', []),
                datasets: [{
                    label: 'Lessons completed',
                    data:  readAttr(actC, 'values', []),
                    backgroundColor: BRAND.primary,
                    borderRadius: 6,
                    borderSkipped: false,
                    barThickness: 36,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { backgroundColor: BRAND.ink } },
                scales: {
                    y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: 'rgba(230,223,206,.5)' } },
                    x: { grid: { display: false } },
                },
            },
        });
    }

    // ─── Member: horse usage donut ───────────────────────────────────────
    const myH = document.getElementById('chart-my-horses');
    if (myH) {
        new Chart(myH, {
            type: 'doughnut',
            data: {
                labels: readAttr(myH, 'labels', []),
                datasets: [{
                    data: readAttr(myH, 'values', []),
                    backgroundColor: palette,
                    borderWidth: 0,
                    hoverOffset: 6,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false, cutout: '60%',
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 10, padding: 12, font: { size: 11 } } },
                    tooltip: { backgroundColor: BRAND.ink },
                },
            },
        });
    }

    // ─── Legacy: horse availability (admin dashboard previous round). Keep
    //     this so any cached page from an old build still works. ────────
    const horseC = document.getElementById('chart-horses');
    if (horseC) {
        const available = parseInt(horseC.dataset.available || '0', 10);
        const total     = parseInt(horseC.dataset.total     || '0', 10);
        new Chart(horseC, {
            type: 'doughnut',
            data: {
                labels: ['Available', 'In Service'],
                datasets: [{
                    data: [available, Math.max(0, total - available)],
                    backgroundColor: [BRAND.primary, BRAND.accent],
                    borderWidth: 0,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false, cutout: '70%',
                plugins: { legend: { position: 'bottom' }, tooltip: { backgroundColor: BRAND.ink } },
            },
        });
    }

    } // end initCharts
})();
