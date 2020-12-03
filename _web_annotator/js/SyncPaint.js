import { PaintTable } from "./PaintTable";
import { SurfaceTable } from "./SurfaceTable";
import crypto from "crypto";
import EventEmitter from "events";
import io from "socket.io-client";

export const socket = io(`${location.origin}/`);
socket.on('system', data => {
  console.log('system', data);
});

const subtract  = function *(a, b) {
  for(const item of a) {
    if(!b.has(item)) {
      yield item;
    }
  }
}

class RoomManager {
  values = new Map();
  emitter = new EventEmitter();
  constructor(socket) {
    this.socket = socket;
    this.socket.on('update', this.onUpdateData);
    this.socket.on('current', this.onUpdateData);
  }
  onUpdateData = data => {
    const currentData = this.values.get(data.room_id);
    if(!currentData || (currentData.sid || this.socket.id) !== this.socket.id || data.sid !== this.socket.id) {
      this.values.set(data.room_id, data);
      this.emitter.emit("update", data);
    }
  }
  enterRoom(roomId) {
    this.socket.emit("enter", roomId)  
  }
  leaveRoom(roomId) {
    this.socket.emit("leave", roomId);
    this.values.delete(roomId);
  }
}

class PaintManager extends RoomManager{
  colors = new Set();
  surfaces = new Set();

  getRoomId({surface, color}) {
    return `${surface}-${color}`;
  }

  addColor(color) {
    for(const surface of this.surfaces) {
      this.enterRoom(this.getRoomId({color, surface}));
    }
    this.colors.add(color);
  }
  removeColor(color) {
    for(const surface of this.surfaces) {
      this.leaveRoom(this.getRoomId({color, surface}));
    }
    this.colors.delete(color);
  }
  addSurface(surface) {
    for(const color of this.colors) {
      this.enterRoom(this.getRoomId({color, surface}));
    }
    this.surfaces.add(surface);
  }
  removeSurface(surface) {
    for(const color of this.colors) {
      this.leaveRoom(this.getRoomId({color, surface}));
    }
    this.surfaces.delete(surface);
  }
  update(data) {
    for(const [objectId, objectData] of Object.entries(data.changes)) {
      for(const [colorId, colorData] of Object.entries(objectData)) {
        const roomId = objectId + "-" + colorId;
        this.values.set(roomId, colorData);
      }
    }
    this.socket.emit("update_paint", data)
  }
  
  // 200116 HU
  updatePaintVolumes() {
    this.socket.emit("update_paint_volumes")
  }
  //
  
  updateList({ list, lastPaintId }) {
    this.socket.emit("update", {
      list,
      lastPaintId,
      room_id: "list"
    })
  }
}


export const paintManager = new PaintManager(socket);

let oldActiveColors = new Set();
export const updatePaintObservation = () => {
  const activeColors = new Set();
  const tableData = PaintTable.getData("active");
  for (const row of tableData) {
    if (row.visibility) {
      activeColors.add(row.id);
    }
  }
  for(const item of subtract(oldActiveColors, activeColors)) {
    paintManager.removeColor(item);
  }
  for(const item of subtract(activeColors, oldActiveColors)) {
    paintManager.addColor(item);
  } 
  oldActiveColors = activeColors;
}
