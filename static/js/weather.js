function fetchJsonData() {
    const url = 'https://api-services.stormgeo.com/api/LocalWeather?kontakttjeneste_id=287050&customer_id=710&sid=9qaa3t4bdjvhhlub78qbsu2sgai2nn0qmk4f03q6';
    console.log("Fetiching");
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            populateTable(data);
            plotWindGraph(data);
            plotHeightGraph(data);
            plotWindWaveGraph(data);
            plotSwellGraph(data);
        })
        .catch(error => {
            console.log('Error displaying forecasts');
        });
}

function formatDateTime(timestep) {
    const date = new Date(timestep);

    const options = { weekday: 'short', hour: '2-digit' };
    return date.toLocaleDateString('en-US', options);
}

function getConfidenceCircle(conf) {
    let color = '';
    switch(conf) {
        case 3:
            color = 'green';
            break;
        case 2:
            color = 'yellow';
            break;
        case 1:
            color = 'red';
            break;
        default:
            color = 'gray';
    }
    return `<span class="confidence-circle" style="background-color: ${color};"></span>`;
}

function populateTable(data) {
    const tableBody = document.querySelector('#weatherTable tbody');
    
    tableBody.innerHTML = '';
    
    data.forEach(item => {
        const row = document.createElement('tr');

        const visibilityInKm = (item.visibility / 1000).toFixed(1);

        const formattedTimestep = formatDateTime(item.timestep);

        let primaryWaveDir = ''
        if(item.primarywavedirection)
            primaryWaveDir = item.primarywavedirection;

        let primaryWavePeriod = ''
        if(item.primarywaveperiod)
            primaryWavePeriod = item.primarywaveperiod;
        
        row.innerHTML = `
            <td>${formattedTimestep}</td>
            <td>${getConfidenceCircle(item.conf)}</td>
            <td>${item.winddirection}</td>
            <td>${item.windspeed}</td>
            <td>${item.windspd_10m_gust}</td>
            <td>${item.windspd_50m}</td>
            <td>${item.windspd_50m_gust}</td>
            <td>${item.waveheigth}</td>
            <td>${item.waveheight_max}</td>
            <td>${item.waveperiod}</td>
            <td>${item.peakperiod_1d}</td>
            <td>${item.secondarywavedirection}</td>
            <td>${item.windwaveheight}</td>
            <td>${item.secondarywaveperiod}</td>
            <td>${primaryWaveDir}</td>
            <td>${item.swellheigth}</td>
            <td>${primaryWavePeriod}</td>
            <td>${item.temperature}</td>
            <td>${visibilityInKm}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

function scrollToGraphs() {
    document.getElementById('graphsSection').scrollIntoView({ behavior: 'smooth' });
}

document.getElementById('skipButton').addEventListener('click', scrollToGraphs);

window.onload = fetchJsonData;

function drawWindArrow(ctx, windDirection) {
    const canvas = document.createElement('canvas');
    const size = 20; // Increase the canvas size for a larger arrow
    canvas.width = size;
    canvas.height = size;
    const arrowCtx = canvas.getContext('2d');
    
    // Set up the arrow drawing based on wind direction
    arrowCtx.translate(size / 2, size / 2);  // Move the origin to the center of the canvas
    arrowCtx.rotate((windDirection * Math.PI) / 180);  // Rotate the canvas to match wind direction
    
    // Draw the arrow shaft (line)
    arrowCtx.beginPath();
    arrowCtx.moveTo(0, 0);  // Start at the center
    arrowCtx.lineTo(0, -size / 2);  // Draw upwards for the shaft
    arrowCtx.strokeStyle = 'black';
    arrowCtx.lineWidth = 2;  // Increase the line width for better visibility
    arrowCtx.stroke();
    
    // Draw the arrowhead (a small triangle at the end)
    arrowCtx.beginPath();
    arrowCtx.moveTo(0, -size / 2);  // Start at the end of the shaft
    arrowCtx.lineTo(size / 6, -size / 3);  // Right point of the triangle
    arrowCtx.lineTo(-size / 6, -size / 3);  // Left point of the triangle
    arrowCtx.closePath();
    arrowCtx.fillStyle = 'black';
    arrowCtx.fill();  // Fill the arrowhead with black
    
    return canvas;  // Return the canvas with the arrow
}

const confidenceBarPlugin = {
    id: 'confidenceBar',
    beforeDraw(chart, args, options) {
        const { ctx, chartArea: { left, right, top }, scales: { x } } = chart;
        const confidenceValues = options.confidenceValues;
        
        ctx.save();
        const barHeight = 15;
        
        // Loop through each confidence value and draw a colored rectangle for each time segment
        confidenceValues.forEach((conf, index) => {
            let color;
            if (conf === 3) {
                color = 'green';
            } else if (conf === 2) {
                color = 'yellow';
            } else {
                color = 'red';
            }

            // Get the x-axis pixel position for each label
            const xPosStart = x.getPixelForValue(index); // Start position of the rectangle
            const xPosEnd = x.getPixelForValue(index + 1) || right; // End position of the rectangle
            
            // Draw the confidence bar as a colored rectangle
            ctx.fillStyle = color;
            ctx.fillRect(xPosStart, top, xPosEnd - xPosStart, barHeight);
        });

        ctx.restore();
    }
};

function plotWindGraph(data) {
    const ctx = document.getElementById('windGraph').getContext('2d');
    
    const labels = data.map(item => formatDateTime(item.timestep));
    
    const windSpeed10m = data.map(item => item.windspeed);
    const windGust10m = data.map(item => item.windspd_10m_gust);
    const windSpeed50m = data.map(item => item.windspd_50m);
    const windGust50m = data.map(item => item.windspd_50m_gust);
    const windDirections = data.map(item => item.winddirection);
    const zeroData = new Array(data.length).fill(0);
    const confidenceValues = data.map(item => item.conf);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Wind Speed 10m (kts)',
                    data: windSpeed10m,
                    borderColor: 'blue',
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Wind Gust 10m (kts)',
                    data: windGust10m,
                    borderColor: 'orange',
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Wind Speed 50m (kts)',
                    data: windSpeed50m,
                    borderColor: 'green',
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Wind Gust 50m (kts)',
                    data: windGust50m,
                    borderColor: 'red',
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Wind Direction',
                    data: zeroData,
                    borderColor: 'black',
                    fill: false,
                    showLine: false,
                    pointRadius: 6,
                    pointStyle: (ctx) => drawWindArrow(ctx, windDirections[ctx.dataIndex]) // Custom arrow points
                },
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Wind Speed / Gust (kts)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Wind Wave',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: {
                        top: 30,
                        bottom: 30
                    }
                },
                confidenceBar: {
                    confidenceValues: confidenceValues,
                }
            }
        },
        plugins: [confidenceBarPlugin]
    });
}

function plotHeightGraph(data) {
    const ctx = document.getElementById('heightGraph').getContext('2d');
    
    const labels = data.map(item => formatDateTime(item.timestep));
    
    const waveheigth = data.map(item => item.waveheigth);
    const waveheigth_max = data.map(item => item.waveheight_max);
    const waveperiod = data.map(item => item.waveperiod);
    const peakperiod_1d = data.map(item => item.peakperiod_1d);
    const confidenceValues = data.map(item => item.conf);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Wave Height (m)',
                    data: waveheigth,
                    borderColor: 'blue',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'yLeft'
                },
                {
                    label: 'Wave Height max (m)',
                    data: waveheigth_max,
                    borderColor: 'orange',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'yLeft'
                },
                {
                    label: 'Wave Period (s)',
                    data: waveperiod,
                    borderColor: 'green',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'yRight'
                },
                {
                    label: 'Peak Period 1d (s)',
                    data: peakperiod_1d,
                    borderColor: 'red',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'yRight'
                },
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                yLeft: {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Height (m)'
                    }
                },
                yRight: {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Period (s)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Wave Height/Period',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: {
                        top: 30,
                        bottom: 30
                    }
                },
                confidenceBar: {
                    confidenceValues: confidenceValues,
                }
            }
        },
        plugins: [confidenceBarPlugin]
    });
}

function plotWindWaveGraph(data) {
    const ctx = document.getElementById('windWaveGraph').getContext('2d');
    
    const labels = data.map(item => formatDateTime(item.timestep));
    
    const windWaveHeight = data.map(item => item.windwaveheight);
    const windWavePeriod = data.map(item => item.secondarywaveperiod);
    const secondarywavedirection = data.map(item => item.secondarywavedirection);
    const zeroData = new Array(data.length).fill(0);
    const confidenceValues = data.map(item => item.conf);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Wind Wave Height (m)',
                    data: windWaveHeight,
                    borderColor: 'blue',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'yLeft'
                },
                {
                    label: 'Wind Wave Period (s)',
                    data: windWavePeriod,
                    borderColor: 'orange',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'yRight'
                },
                {
                    label: 'Wave Direction',
                    data: zeroData,
                    borderColor: 'black',
                    fill: false,
                    showLine: false,
                    pointRadius: 6,
                    yAxisID: 'yRight',
                    pointStyle: (ctx) => drawWindArrow(ctx, secondarywavedirection[ctx.dataIndex])
                },
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                yLeft: {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Height (m)'
                    }
                },
                yRight: {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Period (s)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Wind Wave',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: {
                        top: 30,
                        bottom: 30
                    }
                },
                confidenceBar: {
                    confidenceValues: confidenceValues,
                }
            }
        },
        plugins: [confidenceBarPlugin]
    });
}

function plotSwellGraph(data) {
    const ctx = document.getElementById('swellGraph').getContext('2d');
    
    const labels = data.map(item => formatDateTime(item.timestep));
    
    const swellHeight = data.map(item => item.swellheigth !== undefined ? item.swellheigth : 0);
    const swellPeriod = data.map(item => item.primarywaveperiod !== undefined ? item.primarywaveperiod : 0);
    const swelldirection = data.map(item => item.primarywavedirection !== undefined ? item.primarywavedirection : 0);
    const zeroData = new Array(data.length).fill(0);
    const confidenceValues = data.map(item => item.conf);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Swell Height (m)',
                    data: swellHeight,
                    borderColor: 'blue',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'yLeft'
                },
                {
                    label: 'Swell Period (s)',
                    data: swellPeriod,
                    borderColor: 'orange',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'yRight'
                },
                {
                    label: 'Swell Direction',
                    data: zeroData,
                    borderColor: 'black',
                    fill: false,
                    showLine: false,
                    pointRadius: 6,
                    yAxisID: 'yRight',
                    pointStyle: (ctx) => drawWindArrow(ctx, swelldirection[ctx.dataIndex])
                },
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                yLeft: {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Height (m)'
                    }
                },
                yRight: {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Period (s)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Swell',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: {
                        top: 30,
                        bottom: 30
                    }
                },
                confidenceBar: {
                    confidenceValues: confidenceValues,
                }
            }
        },
        plugins: [confidenceBarPlugin]
    });
}

