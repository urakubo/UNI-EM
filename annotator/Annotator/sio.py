# Socket.ioイベント処理 

from urllib.parse import parse_qs
import socketio

from annotator.Annotator import room

sio = socketio.AsyncServer(async_mode='tornado')

@sio.event
async def update(sid, data):
  session = await sio.get_session(sid)
  room_id = session['room_id']

  room.update_room(room_id, data)

  await sio.emit('update', room.get_room(room_id), room=room_id, skip_sid=sid)

@sio.event
async def disconnect_request(sid):
  await sio.disconnect(sid)

@sio.event
async def connect(sid, environ):
  room_id = parse_qs(environ.get('QUERY_STRING'))['room_id'][0] # ToDo: エラー処理
  
  await sio.save_session(sid, { 'room_id': room_id })
  sio.enter_room(sid, room_id)

  await sio.emit('current', room.get_room(room_id), room=sid)

@sio.event
def disconnect(sid):
  print('Client disconnected')
