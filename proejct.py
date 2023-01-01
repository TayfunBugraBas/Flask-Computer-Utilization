import psutil
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from threading import Event
from datetime import datetime
import os
import psycopg2

#db = psycopg2.connect(
#    host="localhost",
#    dbname="utilizationmonitordb",
#    port="5432",
#    user="postgres",
#    password="1234")

#cursor  = db.cursor()


thread = None
thread_lock = Lock()
thread_event = Event()
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
    
@app.route('/diskiocounters', methods=['GET','POST'])
def dislioCNT():
    
    return render_template('diskiocounters.html')

@app.route('/diskUsages', methods=['GET','POST'])
def diskUsg():
    
    return render_template('diskusages.html')

@app.route('/cpuPercentageList', methods=['GET','POST'])
def cpuPercentageList():
    
    return render_template('diskusages.html')


###function Block ###  



def background_thread(event):
    global thread
    dataDelay = 0
    try:
     while event.is_set():
        sensor_value = psutil.cpu_percent(interval=1)
        
        
        socketio.emit('updateSensorData', {'value':sensor_value,"date": get_current_datetime()})
        socketio.sleep(1)
        dataDelay = dataDelay + 1
        if dataDelay == 120:
 #           cursor.execute(("INSERT INTO f_cpupercent (cpupercent,Date) VALUES(%s,%s);"),(sensor_value,str(get_current_datetime())))
  #          db.commit()
            dataDelay = 0
    finally:
       event.clear()
       thread = None
       
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


def thread_For_Cpu_times(event):
    dataDelay = 0
    while event.is_set():
        times = psutil.cpu_times_percent(interval=1) 
        socketio.emit('cputime', {'valUsr':times[0],'valIdl':times[2],'valSys':times[1],'valIntr':times[3],'valDpc':times[4] ,"dt":get_current_datetime()})
        socketio.sleep(1)
        dataDelay = dataDelay + 1
        if dataDelay == 120:
            
   #         cursor.execute(("INSERT INTO cputimes  VALUES(%s,%s,%s,%s,%s,%s);"),(times[0],times[1],times[2],times[3],times[4],str(get_current_datetime())))
    #        db.commit()
            
            dataDelay = 0
        
def Disk_io_counters(event):
   
    while event.is_set():
        diskio = psutil.disk_io_counters() 
        print(diskio)
        socketio.emit('diskiocount', {'rdCT':diskio[0],'wrCT':diskio[1],'rdBY':diskio[2],'wrBY':diskio[3] ,"dt":get_current_datetime()})
        socketio.sleep(1)
       
        
def DiskUsages(event):
    
    if event.is_set():
     diskUsages = psutil.disk_usage(os.getcwd())
     socketio.emit('diskUsg', {'Total':diskUsages[0],'Used':diskUsages[1],'Free':diskUsages[2]})
     socketio.sleep(1)
    
    
###Event listener Block ###    

@socketio.on('disconnect')
def disconnect():
    global thread
    print('Client disconnected',  request.sid)
    thread_event.clear()
    with thread_lock:
        if thread is not None:
            thread.join()
            thread = None

@socketio.on('cpuTimeButton')
def CpuTimeEvnList():
   global thread
   
   thread_event.set()
   thread = socketio.start_background_task(thread_For_Cpu_times(thread_event),thread_event)
   
@socketio.on('cpuPercentButton')
def CpuPerEvnList():
    global thread
    
    thread_event.set()
    thread = socketio.start_background_task(background_thread(thread_event),thread_event)
    
    
@socketio.on('diskio')
def DiskioCounters():
    global thread
        
    thread_event.set()
    thread = socketio.start_background_task(Disk_io_counters(thread_event),thread_event)

@socketio.on('diskUsageButton')
def DiskUsg():
    global thread
        
    thread_event.set()
    thread = socketio.start_background_task(DiskUsages(thread_event),thread_event)


if __name__ == "__main__":
 socketio.run(app,allow_unsafe_werkzeug=True)
