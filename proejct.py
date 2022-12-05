import psutil
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime

thread = None
thread_lock = Lock()

rule = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')
###Router Block ###
@app.route('/', methods=['GET','POST'])
def index():
   
    return render_template('index.html')
   
    


@app.route('/cpuTimes', methods=['GET','POST'])
def cpuTimes():
    
    return render_template('cpuTimes.html')
    
###function Block ###  

def background_thread(rule):
    
    while rule == '/':
        sensor_value = psutil.cpu_percent()
        print("cpupercent")
        socketio.emit('updateSensorData', {'value':sensor_value,"date": get_current_datetime()})
        socketio.sleep(1)
        
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


def thread_For_Cpu_times(rule):
    
    while rule == '/cpuTimes':
        times = psutil.cpu_times_percent().user
        print("cputime")
        socketio.emit('cputime', {'val':times, "dt":get_current_datetime()})
        socketio.sleep(1)

###Event listener Block ###    

@socketio.on('disconnect')
def disconnect():
    global thread
    print('Client disconnected',  request.sid)
    thread = None

@socketio.on('cpuTimeButton')
def CpuTimeEvnList():
   global thread
   rule = '/cpuTimes'
   thread = socketio.start_background_task(thread_For_Cpu_times(rule))
   
@socketio.on('cpuPercentButton')
def CpuPerEvnList():
    global thread
    rule = '/'
    thread = socketio.start_background_task(background_thread(rule))
    

if __name__ == "__main__":
 socketio.run(app,allow_unsafe_werkzeug=True)
