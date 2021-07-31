
var socket = io();

const config4 = {
  type: 'line',
  data: {
    labels: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    datasets: [{
      label: 'Presion atmosferica vs Tiempo',
      borderColor: "rgb(204, 37, 41)",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      tension: 0.3,
      fill: false,
      showLine: true,
      spanGaps: false,

    }],
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Sensor de Barometrico'
      },

    },
    scales: {
      y: {
        min: 0,
        max: 1100,
      },
    }
  },

};
var ctx = document.getElementById('myChart4').getContext('2d');
grafica4 = new Chart(ctx, config4);
socket.on('mqtt_message4', function (valor) {

  recValue = valor['presion']
  recDate = valor['fecha2']
  // console.log(valor)
  document.getElementById('value4').innerHTML = recValue;

  if (config4.data.labels.length == 10) {
    config4.data.labels.shift();
    config4.data.datasets[0].data.shift();
  }
  config4.data.labels.push(recDate)
  config4.data.datasets[0].data.push(recValue)
  grafica4.update();

});
