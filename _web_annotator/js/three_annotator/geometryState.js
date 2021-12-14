class GeometryColor {
  constructor(length) {
    this.painted = new Int8Array(length);
    this.totalArea = 0;
    this.updated = false;
  }
  clear() {
    this.painted.fill(0);
    this.totalArea = 0;
  }
}

class GeometryState {
  totalArea = 0;
  geometryColors = {};
  constructor(geometry) {
    this.geometry = geometry;
    this.initArea();
  }
  initArea() {
    const vertexCount = this.geometry.attributes.position.count;
    const faceCount = vertexCount / 3;
    this.areas = new Float32Array(faceCount);
    const positionArray = this.geometry.attributes.position.array;
    const length = positionArray.length;
    for (let i = 0; i < length; i += 9) {
      const face_area = calcArea(
        positionArray[i + 0],
        positionArray[i + 1],
        positionArray[i + 2],
        positionArray[i + 3],
        positionArray[i + 4],
        positionArray[i + 5],
        positionArray[i + 6],
        positionArray[i + 7],
        positionArray[i + 8]
      );
      this.areas[i / 9] = face_area / 3;
    }
  }
  activeColors = [0, 1, 2];
  targetColorId = 0;
  colorParams = {
    0: { r: 1, g: 0, b: 0 },
    1: { r: 0, g: 1, b: 0 },
    2: { r: 0, g: 0, b: 1 },
    eraser: { r: 1, g: 1, b: 1 },
  };
  eraserColorId = "eraser";
  overwrite = true;


  getChanges() {
    const response = {};
    for (const colorId of this.activeColors) {
      const geometryColor = this.geometryColors[colorId];
      if(geometryColor?.updated) {
        response[colorId] = {
          painted: geometryColor.painted,
          totalArea: geometryColor.totalArea, 
        };
        geometryColor.updated = false;
      }
    } 
    return response;
  }

  setAnnotation(colorId, data) {
    const geometryColor = this.getGeometryColor(colorId);
    if(data.painted) {
      geometryColor.painted = data.painted;
      geometryColor.totalArea = data.totalArea;
      this.updateAllColor();
    }
  }

  getGeometryColor(colorId) {
    if (!this.geometryColors[colorId]) {
      const vertexCount = this.geometry.attributes.position.count;
      this.geometryColors[colorId] = new GeometryColor(vertexCount);
    }
    return this.geometryColors[colorId];
  }
  updateAllColor() {
    const colorArray = this.geometry.attributes.color.array;
    const vertexCount = colorArray.length / 3;
    for (let i = 0; i < vertexCount; i += 1) {
      this.updateColor(i);
    }
    this.geometry.attributes.color.needsUpdate = true;
    this.geometry.colorsNeedUpdate = true;
  }
  updateColor(vertexIndex) {
    let effecientColorId = this.eraserColorId;
    for (const colorId of this.activeColors) {
      if (this.geometryColors[colorId]?.painted[vertexIndex]) {
        effecientColorId = colorId;
        break;
      }
    }
    const colorArray = this.geometry.attributes.color.array;
    const colorParam = this.colorParams[effecientColorId];
    colorArray[vertexIndex * 3 + 0] = colorParam.r;
    colorArray[vertexIndex * 3 + 1] = colorParam.g;
    colorArray[vertexIndex * 3 + 2] = colorParam.b;
  }

//////////////
  getColorId(vertexIndex) {
	  var ids  = [];
	  for (const colorId of this.activeColors) {
	    const geometryColor = this.getGeometryColor(colorId);
		if (geometryColor.painted[vertexIndex] == 1) {
			ids.push(colorId);
			}
		}
	  return ids;
  }
//////////////


  setColor(vertexIndex) {
    if (this.overwrite) {
      for (const colorId of this.activeColors) {
        const geometryColor = this.getGeometryColor(colorId);
        if (colorId === this.targetColorId) {
          if (geometryColor.painted[vertexIndex] === 0) {
            geometryColor.painted[vertexIndex] = 1;
            geometryColor.totalArea += this.areas[Math.floor(vertexIndex / 3)];
            geometryColor.updated = true;
          }
        } else {
          if (geometryColor.painted[vertexIndex] === 1) {
            geometryColor.painted[vertexIndex] = 0;
            geometryColor.totalArea -= this.areas[Math.floor(vertexIndex / 3)];
            geometryColor.updated = true;
          }
        }
      }
      const colorArray = this.geometry.attributes.color.array;
      const colorParam = this.colorParams[
        this.eraser ? this.eraserColorId : this.targetColorId
      ];
      colorArray[vertexIndex * 3 + 0] = colorParam.r;
      colorArray[vertexIndex * 3 + 1] = colorParam.g;
      colorArray[vertexIndex * 3 + 2] = colorParam.b;
      return true;
    } else if (this.eraser) {
      const geometryColor = this.getGeometryColor(this.targetColorId);
      if (geometryColor.painted[vertexIndex] === 1) {
        geometryColor.painted[vertexIndex] = 0;
        geometryColor.totalArea -= this.areas[Math.floor(vertexIndex / 3)];
        geometryColor.updated = true;
        this.updateColor(vertexIndex);
        return true;
      }
    } else {
      const geometryColor = this.getGeometryColor(this.targetColorId);
      if (geometryColor.painted[vertexIndex] === 0) {
        geometryColor.painted[vertexIndex] = 1;
        geometryColor.totalArea += this.areas[Math.floor(vertexIndex / 3)];
        geometryColor.updated = true;
        this.updateColor(vertexIndex);
        return true;
      }
    }
  }

  setColorOptions({
    targetColorId,
    activeColors,
    colorParams,
    eraserColorId,
    eraser,
    overwrite,
  }) {
    this.activeColors = activeColors || this.activeColors;
    this.eraserColorId = eraserColorId || this.eraserColorId;
    this.colorParams = colorParams || this.colorParams;
    this.eraser = eraser != null ? eraser : this.eraser;
    this.overwrite = overwrite != null ? overwrite : this.overwrite;
    this.targetColorId = this.eraser && this.overwrite
      ? this.eraserColorId
      : this.activeColors[0];
    this.updateAllColor();
  }

  setColorParams(colorParams) {
    this.colorParams = colorParams;
    this.updateAllColor();
  }
  annotate({ center, direction, limit, ignoreBackFace }) {
    window.geometryState = this;
    const geometry = this.geometry;
    const center_x = center.x,
      center_y = center.y,
      center_z = center.z;
    const direction_x = direction.x,
      direction_y = direction.y,
      direction_z = direction.z;
    let needsUpdate = false;
    if (geometry.isBufferGeometry) {
      const positionArray = geometry.attributes.position.array;
      const normalArray = geometry.attributes.normal.array;
      const length = positionArray.length;
      for (let i = 0; i < length; i += 3) {
        const x = positionArray[i + 0] - center_x;
        const y = positionArray[i + 1] - center_y;
        const z = positionArray[i + 2] - center_z;
        if (x * x + y * y + z * z > limit) {
          continue;
        }
        if (ignoreBackFace) {
          if (
            normalArray[i + 0] * direction_x +
              normalArray[i + 1] * direction_y +
              normalArray[i + 2] * direction_z <
            0
          ) {
            continue;
          }
        }
        const hasUpdated = this.setColor(i / 3);
        if (hasUpdated) {
          needsUpdate = true;
        }
      }
      if (needsUpdate) {
        geometry.attributes.color.needsUpdate = true;
        geometry.colorsNeedUpdate = true;
        return true;
      }
    }
  }

///////////////////////////
  getPaintID(center) {
    //window.geometryState = this;
    const geometry = this.geometry;
    const center_x = center.x,
      center_y = center.y,
      center_z = center.z;
    const positionArray = geometry.attributes.position.array;
    const length = positionArray.length;

    var x = positionArray[0] - center_x;
    var y = positionArray[1] - center_y;
    var z = positionArray[2] - center_z;
    var dist  = x * x + y * y + z * z
    var i_min = 0
    for (let i = 0+3; i < length; i += 3) {
        x = positionArray[i + 0] - center_x;
        y = positionArray[i + 1] - center_y;
        z = positionArray[i + 2] - center_z;
        const d = x * x + y * y + z * z
        if (d < dist) {
          i_min = i;
          dist  = d;
        }
    }
    const ids = this.getColorId(i_min / 3);
    return ids;
  }
///////////////////////////

  getCurrentParams() {
    let area = 0;
    const areas = Object.keys(this.geometryColors).map(colorId => {
      const partArea = this.geometryColors[colorId]?.totalArea;
      area += partArea;
      return {
        colorId,
        area: partArea,
      };
    });
    return {
      area,
      areas,
    };
  }
}

class GeometryStateMap {
  map = new WeakMap();
  get(geometry) {
    if (!this.map.has(geometry)) {
      this.map.set(geometry, new GeometryState(geometry));
    }
    return this.map.get(geometry);
  }
}
const geometryStateMap = new GeometryStateMap();
export const getGeometryState = geometry => geometryStateMap.get(geometry);

const calcArea = (x1, y1, z1, x2, y2, z2, x3, y3, z3) => {
  const a1 = x1 - x3;
  const b1 = y1 - y3;
  const c1 = z1 - z3;
  const a2 = x2 - x3;
  const b2 = y2 - y3;
  const c2 = z2 - z3;
  const p1 = b1 * c2 - b2 * c1;
  const p2 = c1 * a2 - c2 * a1;
  const p3 = a1 * b2 - a2 * b1;
  return (p1 * p1 + p2 * p2 + p3 * p3) / 2;
};
