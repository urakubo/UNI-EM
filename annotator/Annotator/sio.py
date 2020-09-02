# Socket.ioイベント処理

from urllib.parse import parse_qs
import socketio
import pickle
import os

from annotator.Annotator import room

sio = socketio.AsyncServer(async_mode='tornado')

def open_file(room_id, type):
  return open(u_info.paint_path + os.sep + room_id + ".pickle", type)

def read_file(room_id):
  data = {}
  try:
    with open_file(room_id, 'rb') as file:
      data = pickle.load(file)
  except FileNotFoundError:
    pass
  finally:
    return data

def write_file(room_id, data):
  os.makedirs(u_info.paint_path, exist_ok=True)
  with open_file(room_id, 'wb') as file:
    pickle.dump(data, file)

@sio.event
async def update_paint(sid, data):
  for object_id, object_data in data["changes"].items():
    for color_id, color_data in object_data.items():
      room_id = object_id + "-" + color_id
      # await sio.emit('update', color_data, room=room_id, skip_sid=sid)
      color_data["sid"] = sid
      write_file(room_id, color_data)
      color_data["room_id"] = room_id
      print('Update', sid, room_id, len(color_data["painted"]))
      await sio.emit('update', color_data, room=room_id)

@sio.event
async def update(sid, data):
  print("update", data)
  room_id = data["room_id"];
  data["sid"] = sid
  write_file(room_id, data)
  await sio.emit('update', data, room=room_id)

@sio.event
async def enter(sid, room_id):
  print('Enter', sid, room_id)
  sio.enter_room(sid, room_id)
  data = read_file(room_id)
  # print(data)
  data["room_id"] = room_id
  await sio.emit('current', data, to=sid)
  await sio.emit('system', { "type": "enter", "room_id": room_id }, to=sid)

@sio.event
async def leave(sid, room_id):
  print('Leave', sid, room_id)
  sio.leave_room(sid, room_id)
  await sio.emit('system', { "type": "leave", "room_id": room_id }, to=sid)

@sio.event
def disconnect(sid):
  print('Client disconnected')

@sio.event
async def connect(sid, env):
  await enter(sid, "list")
  await sio.emit('system', { "type": "connected" }, to=sid)


def set_u_info(_u_info):
  global u_info
  u_info = _u_info
