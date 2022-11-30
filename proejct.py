import psutil
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime

thread = None
thread_lock = Lock()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/', methods=['GET','POST'])
def index():
    
    return render_template('index.html')

def background_thread():
    print("Generating random sensor values")
    while True:
        sensor_value = psutil.cpu_percent()
        times = psutil.cpu_times_percent().user
        socketio.emit('updateSensorData', {'value':sensor_value,"date": get_current_datetime()})
        socketio.emit('cputime', {'val':times, "dt":get_current_datetime()})

        socketio.sleep(1)
        
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


     

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)



if __name__ == "__main__":
 socketio.run(app,allow_unsafe_werkzeug=True)
