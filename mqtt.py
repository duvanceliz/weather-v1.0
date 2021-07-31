import eventlet
from flask import Flask, Response, stream_with_context
from flask_mqtt import Mqtt 
from flask_socketio import SocketIO
import json
from flask_sqlalchemy import SQLAlchemy
from app import sensor1

# eventlet.monkey_patch()

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 0.001  # refresh time in seconds
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///prueba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

mqtt = Mqtt(app)
# socketio = SocketIO(app)
db = SQLAlchemy(app)

    
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('duvan/sensores')
    mqtt.subscribe('manuel/sensores')
    mqtt.subscribe('eudes/sensores')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    
    if message.topic == 'duvan/sensores':
        my_json1 = message.payload.decode('utf8')
        data1 = json.loads(my_json1)
        # Datos_recibido = sensor1(dato = data1['temp'])
        # db.session.add(Datos_recibido)
        # db.session.commit()
        print(data1)
        
        
        # socketio.emit('mqtt_message1', data1)
    elif(message.topic == 'manuel/sensores'):
        my_json2 = message.payload.decode('utf8')
        data2 = json.loads(my_json2)
        # socketio.emit('mqtt_message2', data2)
    elif(message.topic == 'eudes/sensores'):
        my_json3 = message.payload.decode('utf8')
        data3 = json.loads(my_json3)
    
         
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level,buf)


if __name__=='__main__': 
    app.run(debug=True)
    mqtt.init_app(app)
    

    # socketio.run(app, host='127.0.0.1', port=5000, use_reloader=False, debug = True)       