// plot.js

document.addEventListener('DOMContentLoaded', function () {
    var temperature_data = {
        x: JSON.parse('{{ sensor_data | map(attribute="timestamp") | list | tojson | safe }}'),
        y: JSON.parse('{{ sensor_data | map(attribute="data.temperature") | list | tojson | safe }}'),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Temperature'
    };

    var temperature_layout = {
        title: 'Temperature Plot',
        xaxis: {
            title: 'Timestamp'
        },
        yaxis: {
            title: 'Temperature'
        }
    };

    Plotly.newPlot('temperature_plot', [temperature_data], temperature_layout);
});