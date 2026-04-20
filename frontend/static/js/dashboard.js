/* ============================================================================
   Dashboard charts
   ----------------------------------------------------------------------------
   Only one chart is set up here: horse utilisation. It reads real values
   from `data-total` / `data-available` attributes that the Django template
   renders from `DashboardView`'s context.

   The previous revenue, lessons-trend and skill-distribution setups were
   removed because they displayed hardcoded placeholder arrays rather than
   real backend data — keeping them running would have misrepresented the
   state of the business to the user.
   ========================================================================= */
(function () {
    'use strict';
    if (typeof Chart === 'undefined') return;

    Chart.defaults.font.family = "'Geist', 'Manrope', -apple-system, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = '#7a7569';
    Chart.defaults.borderColor = 'rgba(230, 223, 206, 0.8)';

    const BRAND = {
        primary: '#1f3a2a',
        accent:  '#b8893a',
        ink:     '#181c18',
    };

    const horseCanvas = document.getElementById('chart-horses');
    if (!horseCanvas) return;

    const available = parseInt(horseCanvas.dataset.available || '0', 10);
    const total     = parseInt(horseCanvas.dataset.total     || '0', 10);
    const inService = Math.max(0, total - available);

    new Chart(horseCanvas, {
        type: 'doughnut',
        data: {
            labels: ['Available', 'In Service'],
            datasets: [{
                data: [available, inService],
                backgroundColor: [BRAND.primary, BRAND.accent],
                borderWidth: 0,
                hoverOffset: 6,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 10, padding: 14, font: { size: 12 } } },
                tooltip: { backgroundColor: BRAND.ink, padding: 10, cornerRadius: 6 },
            },
        },
    });
})();
