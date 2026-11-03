let elbowChartInstance = null;
let silhouetteChartInstance = null;
let pcaChartInstance = null;

const chartColors = [
    '#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', 
    '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#6366f1'
];

const charts = {
    renderElbow(kValues, inertias) {
        const ctx = document.getElementById('elbowChart').getContext('2d');
        if (elbowChartInstance) elbowChartInstance.destroy();

        elbowChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: kValues,
                datasets: [{
                    label: 'Inertia (SSE)',
                    data: inertias,
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    borderWidth: 2,
                    tension: 0.2,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `Inertia: ${ctx.parsed.y.toLocaleString()}`
                        }
                    }
                },
                scales: {
                    x: { title: { display: true, text: 'Số cụm K' } },
                    y: { title: { display: true, text: 'Inertia' } }
                }
            }
        });
    },

    renderSilhouette(kValues, scores) {
        const ctx = document.getElementById('silhouetteChart').getContext('2d');
        if (silhouetteChartInstance) silhouetteChartInstance.destroy();

        silhouetteChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: kValues,
                datasets: [{
                    label: 'Silhouette Score',
                    data: scores,
                    backgroundColor: '#10b981',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { title: { display: true, text: 'Số cụm K' } },
                    y: { min: -1, max: 1, title: { display: true, text: 'Silhouette Score (-1 đến 1)' } }
                }
            }
        });
    },

    renderPCA(pcaData, pcaCentroids) {
        const ctx = document.getElementById('pcaChart').getContext('2d');
        if (pcaChartInstance) pcaChartInstance.destroy();

        // Gom các điểm theo cluster
        const clusters = {};
        pcaData.forEach(pt => {
            if (!clusters[pt.cluster]) clusters[pt.cluster] = [];
            clusters[pt.cluster].push({ x: pt.pc1, y: pt.pc2, id: pt.id });
        });

        const datasets = [];

        // Thêm các điểm sinh viên theo cụm
        Object.keys(clusters).forEach((cIdx) => {
            const color = chartColors[cIdx % chartColors.length];
            datasets.push({
                label: `Cụm ${cIdx}`,
                data: clusters[cIdx],
                backgroundColor: color,
                pointRadius: 6,
                pointHoverRadius: 8
            });
        });

        // Thêm tâm cụm (Centroids)
        datasets.push({
            label: 'Tâm cụm (Centroid)',
            data: pcaCentroids.map(c => ({ x: c.pc1, y: c.pc2 })),
            backgroundColor: '#000000',
            pointStyle: 'crossRot',
            pointRadius: 10,
            pointHoverRadius: 12,
            borderWidth: 3
        });

        pcaChartInstance = new Chart(ctx, {
            type: 'scatter',
            data: { datasets },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (ctx) => {
                                const pt = ctx.raw;
                                const label = ctx.dataset.label || '';
                                return pt.id ? `${pt.id} (${label}): (${pt.x}, ${pt.y})` : `${label}: (${pt.x}, ${pt.y})`;
                            }
                        }
                    }
                },
                scales: {
                    x: { title: { display: true, text: 'Thành phần chính 1 (PC1)' } },
                    y: { title: { display: true, text: 'Thành phần chính 2 (PC2)' } }
                }
            }
        });
    }
};
