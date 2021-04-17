import redis

# r = redis.Redis(
# host='127.0.0.1',
# port='6379',
# password='')

# r.set('ad', 'bar')
# value = r.keys("*")
# print(value)

import socketio
from flask import Flask, render_template


mgr = socketio.RedisManager('redis://')
sio = socketio.Server(client_manager=mgr, async_mode='threading', logger=True, engineio_logger=True)

app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# @sio.event
# def salutations(sid, data):
#     print(f"my event is {sid}, {data}")

def update_driver(driver_id):
    """ Updates one driver """
    print(f"driver-{driver_id} changed!")

@sio.on('position')
def position(sid,driver_id, data):
    """ Called when driver sends new position """
    
    update_driver(driver_id)
    

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event(namespace='/chat')
def my_custom_event(sid, data):
    pass

@sio.on('my custom event', namespace='/chat')
def my_custom_event(sid, data):
    pass

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@app.route('/driver/<driver_id>')
def driver(driver_id):

    print(f"Driver with id {driver_id} connected!")
    return render_template('driver.html', driver_id = driver_id)

if __name__ == '__main__':
    app.run(threaded=True, debug=True)