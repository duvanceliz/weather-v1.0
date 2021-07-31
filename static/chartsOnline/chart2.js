
var socket = io();

const config2 = {
  type: 'line',
  data: {
    labels: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    datasets: [{
      label: 'Temperatura vs Tiempo',
      borderColor: "rgb(218, 124, 48)",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      tension: 0.3,
      fill: false,
      showLine: true,
      spanGaps: false,

    }],
  },
  options: {
    plugins: {
      title: {
        display: true,
        text: 'Sensor de Temperatura'
      },

    },
  },

};
var ctx = document.getElementById('myChart2').getContext('2d');
grafica2 = new Chart(ctx, config2);
socket.on('mqtt_message2', function (valor) {

  recValue = valor['temp']
  recDate = valor['fecha']
  // console.log(valor)
  document.getElementById('value2').innerHTML = recValue;

  if (config2.data.labels.length == 10) {
    config2.data.labels.shift();
    config2.data.datasets[0].data.shift();
  }
  config2.data.labels.push(recDate)
  config2.data.datasets[0].data.push(recValue)
  grafica2.update();

});