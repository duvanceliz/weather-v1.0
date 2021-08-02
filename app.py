from flask import Flask, render_template, request, session, escape, redirect, url_for, flash, g, send_from_directory,jsonify,send_file,Response,stream_with_context
from flask_sqlalchemy import SQLAlchemy
from werkzeug import debug
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user,logout_user,login_required,current_user,UserMixin
from datetime import datetime
from flask_mqtt import Mqtt 
import json
import pandas as pd
from flask_mail import Mail
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'duvanceliz@gmail.com'
app.config['MAIL_PASSWORD'] = 'ingmusica2020'
app.config['MAIL_DEFAULT_SENDER'] = 'duvanceliz@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None

app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 0.001  # refresh time in seconds


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///prueba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost/test'

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{database}".format(
#     username = 'root',
#     password = '123456',
#     hostname = 'localhost',
#     database = 'test'
# )

# UPLOAD_FOLDER = os.path.abspath('./static/')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'bx99xa4xa6x1axc9x10irxfexdeex12x0esx98'


mqtt = Mqtt(app)

mail = Mail(app)
db = SQLAlchemy(app)
s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'],expires_in=3600)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'iniciarsesion' 

class usuarios(UserMixin,db.Model):
    __tablename__='usuarios'
    id = db.Column(db.Integer,  primary_key = True)
    nombre = db.Column(db.String(50), unique= True,nullable=False)
    contraseña = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(50), unique=True,nullable=False)
    fecha = db.Column(db.DateTime, default = datetime.now)
    def __repr__(self):
        return self.nombre

class sensor1(db.Model):
    __tablename__= 'sensor1'
    id = db.Column(db.Integer,  primary_key = True)
    dato = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default = datetime.now) 
    
class sensor2(db.Model):
    __tablename__= 'sensor2'
    id = db.Column(db.Integer,  primary_key = True)
    dato = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default = datetime.now) 

class sensor3(db.Model):
    __tablename__= 'sensor3'
    id = db.Column(db.Integer,  primary_key = True)
    dato = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default = datetime.now) 

class sensor4(db.Model):
    __tablename__= 'sensor4'
    id = db.Column(db.Integer,  primary_key = True)
    dato = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default = datetime.now)


@login_manager.user_loader
def load_user(user_id):
    return usuarios.query.get(int(user_id))

@app.route('/',methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    
    if not current_user.is_authenticated:
        if request.method == 'POST':

            lon_nom =len(request.form.get('nombre'))
            lon_pass =len(request.form.get('clave')) 
            lon_email =len(request.form.get('email')) 
            if lon_nom != 0 and lon_email != 0 and lon_pass != 0:

                nombre_existente = usuarios.query.filter_by(nombre=request.form.get('nombre')).first()
                email_existente = usuarios.query.filter_by(email=request.form.get('email')).first()

                if nombre_existente:
                    flash('El nombre de usuario ya existe, intenta con otro', 'error')
                elif email_existente:
                    flash('El correo proporcionado ya existe, intenta con otro', 'error')
                elif request.form.get('clave') != request.form.get('confirClave'):
                    flash('La contraseña proporcionada no coincide','error')

                else:

                    codificar_clave = generate_password_hash(request.form.get('clave'), method = 'sha256')
                    nuevo_usuario = usuarios(nombre = request.form.get('nombre'), contraseña = codificar_clave, email= request.form.get('email') ) 
                    db.session.add(nuevo_usuario)
                    db.session.commit()
                    # msg = Message('Gracias por registrarte!', sender= app.config['MAIL_USERNAME'], recipients=[request.form.get('email')])
                    # msg.html = render_template('email.html', user = request.form.get('nombre'))
                    # mail.send(msg)

                    flash(' Te has registrado exitosamente.','exito')

                    return redirect(url_for('iniciarsesion'))
            else:
                flash('No dejes espacios en blanco, todos los campos son abligatorios','error')
        
        return render_template('registro.html')
    return redirect(url_for('perfil'))


@app.route('/iniciarsesion',methods=['GET','POST'])
def iniciarsesion():
    if not current_user.is_authenticated:
        if request.method == 'POST':

            usuario = usuarios.query.filter_by(nombre = request.form.get('nombre')).first()

            if usuario and check_password_hash(usuario.contraseña, request.form.get('clave')):

                login_user(usuario, remember=request.form.get('recordar'))
            
                return redirect('/perfil')
            
            flash('La contraseña o el usuario no coinciden','error')

        return render_template('login.html')
    return redirect('/perfil')

@app.route('/perfil', methods=['GET','POST'])
@login_required
def perfil():
    user = current_user
    return render_template('perfil.html', user=user)

@app.route('/salir')
@login_required
def salir():
    logout_user()
    return redirect('/')

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/acomulados',methods=['GET', 'POST'])
def acomulados():

    wSensor = sensor1.query.order_by(sensor1.fecha.asc()).all()
    size = len(wSensor)
    if size >= 20:
        wSensor20 = wSensor[size-20:size]
    else:
        wSensor20 = wSensor
    name = 'Sensor de agua'
    color = 'rgb(57, 106, 177)'
    label = 'nivel de agua vs tiempo'

    if request.method == 'POST':
        stsend = request.form.get('sensorType')
        dateSend = request.form.get('date')
        timeSend = request.form.get('time')
        if stsend == '1':
            query = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            allsensor1 = sensor1.query.filter(sensor1.fecha.like(query)).all()
            wSensor20 = allsensor1
            name = 'Sensor de Agua'
            color = 'rgb(57, 106, 177)'
            label = 'Nivel de agua vs tiempo'
        elif stsend == '2':
            query = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            allsensor2 = sensor2.query.filter(sensor2.fecha.like(query)).all()
            wSensor20 = allsensor2
            name = 'Sensor de Temperatura'
            color = 'rgb(218, 124, 48)'
            label = 'Temperatura vs Tiempo'
        elif stsend == '3':
            query = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            allsensor3 = sensor3.query.filter(sensor3.fecha.like(query)).all()
            wSensor20 = allsensor3
            name = 'Sensor de Humedad'
            color = 'rgb(62, 150, 81)'
            label = 'Humedad vs Tiempo'
        elif stsend == '4':
            query = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            allsensor4 = sensor4.query.filter(sensor4.fecha.like(query)).all()
            wSensor20 = allsensor4
            name = 'Sensor Barometrico'
            color = 'rgb(204, 37, 41)'
            label = 'Presion atmosferica vs Tiempo'


    return render_template('acomulados.html',wSensor20 = wSensor20, name= name, color=color, label=label )

@app.route('/downloadData',methods=['GET', 'POST'])
def downloadData():      
    return render_template('downloadData.html')

@app.route('/download',methods=['GET', 'POST'])
def download():
    data = []
    date = []
    if request.method == 'POST':
        dateSend = request.form.get('date')
        timeSend = request.form.get('time')
        stSend = request.form.get('sensorType')
        if stSend == '1':
            format = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            sensorQuery1 = sensor1.query.filter(sensor1.fecha.like(format)).all()
            if sensorQuery1 != []:
                for i in sensorQuery1:
                    data.append(i.dato)
                    date.append(i.fecha.strftime('%m/%d/%Y--%H:%M:%S'))
                dict = {'Nivel de Agua': data, 'fecha': date} 
                df = pd.DataFrame(dict) 
                df.to_csv('datos.csv') 
                p = 'datos.csv' 
                return send_file(p,as_attachment=True)
            else:
                flash('No hay datos para la fecha ingresada','error')
                return redirect('/downloadData')
        elif stSend == '2':
            format = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            sensorQuery2 = sensor2.query.filter(sensor2.fecha.like(format)).all()
            if sensorQuery2 != []:
                for i in sensorQuery2:
                    data.append(i.dato)
                    date.append(i.fecha.strftime('%m/%d/%Y--%H:%M:%S'))
                dict = {'Temperatura': data, 'fecha': date} 
                df = pd.DataFrame(dict) 
                df.to_csv('datos.csv') 
                p = 'datos.csv' 
                return send_file(p,as_attachment=True)
            else:
                flash('No hay datos para la fecha ingresada','error')
                return redirect('/downloadData')
        elif stSend == '3':
            format = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            sensorQuery3 = sensor3.query.filter(sensor3.fecha.like(format)).all()
            if sensorQuery3 != []:
                for i in sensorQuery3:
                    data.append(i.dato)
                    date.append(i.fecha.strftime('%m/%d/%Y--%H:%M:%S'))
                dict = {'Humedad': data, 'fecha': date} 
                df = pd.DataFrame(dict) 
                df.to_csv('datos.csv') 
                p = 'datos.csv' 
                return send_file(p,as_attachment=True)
            else:
                flash('No hay datos para la fecha ingresada','error')
                return redirect('/downloadData')
        elif stSend == '4':
            format = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            sensorQuery4 = sensor4.query.filter(sensor4.fecha.like(format)).all()
            if sensorQuery4 != []:
                for i in sensorQuery4:
                    data.append(i.dato)
                    date.append(i.fecha.strftime('%m/%d/%Y--%H:%M:%S'))
                dict = {'Humedad': data, 'fecha': date} 
                df = pd.DataFrame(dict) 
                df.to_csv('datos.csv') 
                p = 'datos.csv' 
                return send_file(p,as_attachment=True)
            else:
                flash('No hay datos para la fecha ingresada','error')
                return redirect('/downloadData')

        else:
            flash('No se pueden descargar datos porque los campos estan vacios o el sensor no existe','error')
            return redirect('/downloadData')

@app.route('/changepassword',methods=['GET', 'POST'])
def changepassword():
    global gtoken
    if request.method == 'POST':
        email_existente = usuarios.query.filter_by(email=request.form.get('emailRec')).first()
        if email_existente != None:
            token= s.dumps(email_existente.email, salt='email-rec').decode('utf-8')
            msg = Message('Recuperar contraseña!', sender= app.config['MAIL_USERNAME'], recipients=[email_existente.email])
            format = "hola para recuperar la contraseña ingresa al siguiente enlace: http://127.0.0.1:5000/recoverpassword/{token}".format(token=token)
            msg.body = format
            mail.send(msg)
        else:
            flash('El correo proporcionado no se encuentra registrado','error')
    return render_template('changepassword.html')

@app.route('/recoverpassword/<token>')
def recoverpassword(token):
    try:
        email = s.loads(token, salt='email-rec')
        userQuery = usuarios.query.filter_by(email = email).first()
    
    except SignatureExpired:
        return render_template('expired.html')
    return render_template('resetpassword.html',userQuery=userQuery ,token = token)


@app.route('/newpassword',methods=['GET', 'POST'])
def newpassword():

    if request.method == 'POST':
        valueToken = request.form.get('valueToken')
        password=request.form.get('clave')
        passwordConf = request.form.get('confirClave')
        userId = request.form.get('user')
        if password == passwordConf:
            userQuery = usuarios.query.filter_by(id = userId).first()
            oldUser = userQuery
            db.session.delete(userQuery)
            db.session.commit()
            codificar_clave = generate_password_hash(password, method = 'sha256')
            newUser = usuarios(nombre = oldUser.nombre, contraseña = codificar_clave , email = oldUser.email )
            db.session.add(newUser)
            db.session.commit()
            flash('La contraseña se ha cambiado con exito','exito')
            return redirect('iniciarsesion')
        else:
            flash('La contraseña no coincide','error')
    rformat = 'recoverpassword/{token}'.format(token= valueToken)  
    print(rformat)
    return redirect(rformat)


def _dato():
    dato = sensor1.query.order_by(sensor1.fecha.desc()).first()
    dato2 = sensor2.query.order_by(sensor2.fecha.desc()).first()
    dato3 = sensor3.query.order_by(sensor3.fecha.desc()).first()
    dato4 = sensor4.query.order_by(sensor4.fecha.desc()).first()
    dict1 = {'dato':dato.dato,'dato2':dato2.dato, 'dato3':dato3.dato,'dato4':dato4.dato,'fecha':dato.fecha.strftime('%H:%M:%S')}
    json_data = json.dumps(dict1)
    yield f"data:{json_data}\n\n"


@app.route('/datos_monitoreo')
def datos_monitoreo():
    enviar = _dato()
    return Response(stream_with_context(enviar), mimetype='text/event-stream')

  
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('duvan/sensores')
    mqtt.subscribe('manuel/sensores')
    mqtt.subscribe('eudes/sensores')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    
    if (message.topic == 'duvan/sensores'):
        my_json1 = message.payload.decode('utf8')
        data1 = json.loads(my_json1)
        Datos_recibido = sensor1(dato = data1['nivel'])
        db.session.add(Datos_recibido)
        db.session.commit()

    elif(message.topic == 'manuel/sensores'):
        my_json2 = message.payload.decode('utf8')
        data2 = json.loads(my_json2)
        Datos_recibido2 = sensor2(dato = data2['nivel'])
        db.session.add(Datos_recibido2)
        db.session.commit()
       
       
    elif(message.topic == 'eudes/sensores'):
        my_json3 = message.payload.decode('utf8')
        data3 = json.loads(my_json3)
        Datos_recibido = sensor3(dato = data3['nivel'])
        db.session.add(Datos_recibido)
        db.session.commit()
        Datos_recibido2 = sensor4(dato = data3['nivel'])
        db.session.add(Datos_recibido2)
        db.session.commit()
       
      
            
# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     print(level,buf)

if __name__=='__main__':
    db.create_all()
    app.run()
    mail.init_app(app)
    mqtt.init_app(app)

