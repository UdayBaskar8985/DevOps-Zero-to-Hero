document.addEventListener("DOMContentLoaded", () => {
    // 1. Category Doughnut Chart
    const categoryCtx = document.getElementById('categoryChart');
    if (categoryCtx && typeof catLabels !== 'undefined' && typeof catValues !== 'undefined') {
        const hasData = catValues.length > 0;
        
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: hasData ? catLabels : ['No Expenses Recorded'],
                datasets: [{
                    data: hasData ? catValues : [1],
                    backgroundColor: hasData ? [
                        '#8b5cf6', // purple
                        '#ec4899', // pink
                        '#3b82f6', // blue
                        '#10b981', // emerald
                        '#f59e0b', // amber
                        '#ef4444', // rose
                        '#06b6d4', // cyan
                        '#64748b'  // slate
                    ] : ['rgba(255, 255, 255, 0.05)'],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#9ca3af',
                            font: {
                                family: 'Outfit',
                                size: 13,
                                weight: '500'
                            },
                            padding: 20
                        }
                    },
                    tooltip: {
                        enabled: hasData,
                        backgroundColor: 'rgba(14, 11, 32, 0.95)',
                        titleColor: '#f3f4f6',
                        bodyColor: '#f3f4f6',
                        borderColor: 'rgba(255, 255, 255, 0.08)',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 10,
                        titleFont: { family: 'Outfit', weight: '600' },
                        bodyFont: { family: 'Outfit' },
                        callbacks: {
                            label: function(context) {
                                return ' Total: $' + context.raw.toFixed(2);
                            }
                        }
                    }
                },
                cutout: '72%'
            }
        });
    }

    // 2. Spending Trend Line Chart
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx && typeof trendLabels !== 'undefined' && typeof trendValues !== 'undefined') {
        const ctx2d = trendCtx.getContext('2d');
        const gradient = ctx2d.createLinearGradient(0, 0, 0, 280);
        gradient.addColorStop(0, 'rgba(139, 92, 246, 0.35)');
        gradient.addColorStop(1, 'rgba(139, 92, 246, 0.0)');

        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: trendLabels,
                datasets: [{
                    label: 'Daily Expenses',
                    data: trendValues,
                    borderColor: '#8b5cf6',
                    borderWidth: 3,
                    fill: true,
                    backgroundColor: gradient,
                    tension: 0.35,
                    pointBackgroundColor: '#8b5cf6',
                    pointBorderColor: 'rgba(255, 255, 255, 0.2)',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#ec4899',
                    pointHoverBorderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#9ca3af',
                            font: { family: 'Outfit', size: 12 }
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#9ca3af',
                            font: { family: 'Outfit', size: 12 },
                            callback: function(value) {
                                return '$' + value;
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(14, 11, 32, 0.95)',
                        titleColor: '#f3f4f6',
                        bodyColor: '#f3f4f6',
                        borderColor: 'rgba(255, 255, 255, 0.08)',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 10,
                        titleFont: { family: 'Outfit', weight: '600' },
                        bodyFont: { family: 'Outfit' },
                        callbacks: {
                            label: function(context) {
                                return ' Spent: $' + context.raw.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
    }
});
