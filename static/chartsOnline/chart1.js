
var socket = io();

const config = {
  type: 'line',
  data: {
    labels: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    datasets: [{
      label: 'Nivel de Agua vs Tiempo',
      borderColor: "rgb(57, 106, 177)",
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
        text: 'Sensor de Agua'
      },

    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Tiempo(h/m/s)',
          font: {
            family: 'Comic Sans MS',
            size: 13,
            weight: 'bold',
            lineHeight: 1,
          },
        }

      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Nivel(%)',
          font: {
            family: 'Comic Sans MS',
            size: 13,
            weight: 'bold',
            lineHeight: 1,
          },

        },
        min: 0,
        max: 100,
      },

    }

  }

};
var ctx = document.getElementById('myChart').getContext('2d');
grafica = new Chart(ctx, config);
socket.on('mqtt_message1', function (valor) {

  recValue = valor['nivel']
  recDate = valor['fecha']
  document.getElementById('value1').innerHTML = Math.round(recValue);
  console.log(valor)

  if (config.data.labels.length == 10) {
    config.data.labels.shift();
    config.data.datasets[0].data.shift();
  }
  config.data.labels.push(recDate)
  config.data.datasets[0].data.push(recValue)
  grafica.update();

});
