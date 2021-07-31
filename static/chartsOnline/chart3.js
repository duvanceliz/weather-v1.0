  
var socket = io();

 const config3 = {
    type: 'line',
    data:{
      labels:[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      datasets:[{
        label:'Humedad vs Tiempo',
        borderColor: "rgb(62, 150, 81)",
        data:[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        text: 'Sensor de Humedad'
    },
  
}
   },
   scales: {
      y: {
      min: 0,
      max: 50,
      },
   }
   
};
  var ctx = document.getElementById('myChart3').getContext('2d');
  grafica3 = new Chart(ctx,config3);
  socket.on('mqtt_message3', function(valor){

  recValue = valor['temp']
  recDate = valor['fecha']
  // console.log(valor)
  document.getElementById('value3').innerHTML = recValue;
  
  if (config3.data.labels.length == 10) {
        config3.data.labels.shift();
        config3.data.datasets[0].data.shift();
    }
  config3.data.labels.push(recDate)
  config3.data.datasets[0].data.push(recValue) 
  grafica3.update();

});
