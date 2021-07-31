
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
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Sensor de Temperatura'
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
          text: 'Temperatura(°C)',
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
  },

};
var ctx = document.getElementById('myChart2').getContext('2d');
grafica2 = new Chart(ctx, config2);
socket.on('mqtt_message2', function (valor) {

  recValue = valor['temp']
  recDate = valor['fecha3']
  console.log(valor)
  document.getElementById('value2').innerHTML = Math.round(recValue);

  if (config2.data.labels.length == 10) {
    config2.data.labels.shift();
    config2.data.datasets[0].data.shift();
  }
  config2.data.labels.push(recDate)
  config2.data.datasets[0].data.push(recValue)
  grafica2.update();

});