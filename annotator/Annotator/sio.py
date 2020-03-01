# Socket.ioイベント処理

from urllib.parse import parse_qs
import socketio

from annotator.Annotator import room

sio = socketio.AsyncServer(async_mode='tornado')

@sio.event
async def update(sid, room_id, data):
  # ToDo: 入力条件
  print('Update', room_id, data)
  room.update_room(room_id, data)
  await sio.emit('update', room.get_room(room_id), room=room_id, skip_sid=sid)

@sio.event
async def disconnect_request(sid):
  await sio.disconnect(sid)

@sio.event
async def enter(sid, room_id):
  # ToDo: 入力条件
  print('Enter', sid, room_id)
  sio.enter_room(sid, room_id)
  await sio.emit('current', room.get_room(room_id), room=sid)

@sio.event
def leave(sid, room_id):
  # ToDo: 入力条件
  print('Leave', sid, room_id)
  sio.leave_room(sid, room_id)

@sio.event
def disconnect(sid):
  print('Client disconnected')
