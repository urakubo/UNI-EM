# Room管理のスタブ

room_data = {
  '/room01': {
    'data': 'this is a room',
  }
}
def get_room(id):
  return {
    'room_id': id,
    'data': room_data[id],
  }

def update_room(id, data):
  room_data[id] = data
