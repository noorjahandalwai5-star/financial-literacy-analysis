/**
 * Financial Literacy Project - Frontend Chart & Visualization Scripts
 * Author: B.Sc Data Science Student
 * Powered by Chart.js
 */

// Global Chart.js defaults
Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
Chart.defaults.color = '#6c757d';

/**
 * Initializes charts on the Dashboard page.
 */
function initDashboardCharts(data) {
    if (!data) return;

    // 1. Donut Chart: Literacy Level Distribution
    const ctxLevel = document.getElementById('levelDistributionChart');
    if (ctxLevel) {
        new Chart(ctxLevel, {
            type: 'doughnut',
            data: {
                labels: ['Basic (<50%)', 'Intermediate (50-75%)', 'Advanced (>75%)'],
                datasets: [{
                    data: [
                        data.level_counts.Basic || 0,
                        data.level_counts.Intermediate || 0,
                        data.level_counts.Advanced || 0
                    ],
                    backgroundColor: ['#ffc107', '#0d6efd', '#198754'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                },
                cutout: '65%'
            }
        });
    }

    // 2. Horizontal Bar Chart: Topic Pass Rates
    const ctxTopics = document.getElementById('topicPassRatesChart');
    if (ctxTopics) {
        const topics = Object.keys(data.topic_pass_rates || {});
        const rates = Object.values(data.topic_pass_rates || {});

        // Color coding: red if < 50%, orange if < 70%, green if >= 70%
        const bgColors = rates.map(rate => {
            if (rate < 50) return 'rgba(220, 53, 69, 0.85)';
            if (rate < 70) return 'rgba(255, 193, 7, 0.85)';
            return 'rgba(25, 135, 84, 0.85)';
        });

        new Chart(ctxTopics, {
            type: 'bar',
            data: {
                labels: topics,
                datasets: [{
                    label: 'Pass Rate (%)',
                    data: rates,
                    backgroundColor: bgColors,
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (ctx) {
                                return ` Pass Rate: ${ctx.raw}% (Knowledge Gap: ${(100 - ctx.raw).toFixed(1)}%)`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        min: 0,
                        max: 100,
                        ticks: { callback: v => v + '%' }
                    }
                }
            }
        });
    }

    // 3. Year Progression Chart
    const ctxYear = document.getElementById('yearProgressionChart');
    if (ctxYear && data.year_comparison) {
        const yearLabels = Object.keys(data.year_comparison);
        const yearScores = yearLabels.map(y => data.year_comparison[y].mean);

        new Chart(ctxYear, {
            type: 'bar',
            data: {
                labels: yearLabels,
                datasets: [{
                    label: 'Average Score (%)',
                    data: yearScores,
                    backgroundColor: 'rgba(13, 110, 253, 0.8)',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: { callback: v => v + '%' }
                    }
                }
            }
        });
    }

    // 4. Financial Education Impact Chart
    const ctxEdu = document.getElementById('eduComparisonChart');
    if (ctxEdu && data.edu_comparison) {
        const eduScores = [
            data.edu_comparison.Yes ? data.edu_comparison.Yes.mean : 0,
            data.edu_comparison.No ? data.edu_comparison.No.mean : 0
        ];

        new Chart(ctxEdu, {
            type: 'bar',
            data: {
                labels: ['With Prior Fin. Education', 'Without Prior Fin. Education'],
                datasets: [{
                    label: 'Average Literacy Score (%)',
                    data: eduScores,
                    backgroundColor: ['rgba(25, 135, 84, 0.85)', 'rgba(220, 53, 69, 0.85)'],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: { callback: v => v + '%' }
                    }
                }
            }
        });
    }
}

/**
 * Initializes charts on the Analytics page.
 */
function initAnalyticsCharts(data) {
    if (!data) return;

    // 1. Budgeting Habits Doughnut
    const ctxBudget = document.getElementById('budgetingPieChart');
    if (ctxBudget && data.budget_dist) {
        new Chart(ctxBudget, {
            type: 'pie',
            data: {
                labels: Object.keys(data.budget_dist),
                datasets: [{
                    data: Object.values(data.budget_dist),
                    backgroundColor: ['#6c757d', '#ffc107', '#0dcaf0', '#198754'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        callbacks: {
                            label: function (ctx) {
                                return ` ${ctx.label}: ${ctx.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    }

    // 2. Saving Habits Bar Chart
    const ctxSaving = document.getElementById('savingHabitsChart');
    if (ctxSaving && data.saving_dist) {
        new Chart(ctxSaving, {
            type: 'bar',
            data: {
                labels: Object.keys(data.saving_dist),
                datasets: [{
                    label: 'Student Percentage (%)',
                    data: Object.values(data.saving_dist),
                    backgroundColor: 'rgba(13, 110, 253, 0.85)',
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        min: 0,
                        max: 60,
                        ticks: { callback: v => v + '%' }
                    }
                }
            }
        });
    }
}

