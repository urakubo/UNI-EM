import { getGeometryState } from "./geometryState";

const getRay = ({ raymouse, camera }) => {
  if (camera && camera.isPerspectiveCamera) {
    return new THREE.Vector3()
      .set(raymouse.x, raymouse.y, 0)
      .unproject(camera)
      .sub(camera.position)
      .normalize();
  } else {
    console.error("Unsupported camera type.");
  }
};
const raycaster = new THREE.Raycaster();
const _getIntersect = ({ raymouse, camera, meshes }) => {
  raycaster.setFromCamera(raymouse, camera);
  const intersects = raycaster.intersectObjects(meshes);
  const intersect = intersects.find(
    intersect => intersect.object.type === "Mesh"
  );
  return intersect;
};

export const getIntersect = ({
  x,
  y,
  camera,
  meshes,
  container,
}) => {
  const raymouse = new THREE.Vector2(
    (x / container.clientWidth) * 2 - 1,
    -(y / container.clientHeight) * 2 + 1
  );
  const intersect = _getIntersect({ raymouse, camera, meshes });
  return {
    intersect
  };
}

export const annotateBySphere = ({
  x,
  y,
  camera,
  meshes,
  container,
  radius,
  ignoreBackFace,
  color,
}) => {
  const raymouse = new THREE.Vector2(
    (x / container.clientWidth) * 2 - 1,
    -(y / container.clientHeight) * 2 + 1
  );
  const intersect = _getIntersect({ raymouse, camera, meshes });
  if (!intersect) {
    return {
      intersect
    }
  }

  const mesh = intersect.object;
  const geometry = mesh.geometry;
  // 高速化のため、逆行列をかけておく
  const center = intersect.point
    .clone()
    .applyMatrix4(new THREE.Matrix4().getInverse(mesh.matrix));
  const scale = mesh.scale.x; // scale.x, scale.y, scale.z are the same
  const limit = (radius * radius) / (scale * scale);
  const direction = getRay({ raymouse, camera });

  const geometryState = getGeometryState(geometry);
  geometryState.annotate({
    center,
    direction,
    limit,
    color,
    ignoreBackFace,
  });
  return {
    intersect
  }
};


///////////////////////////////
export const getPaintID = ({
  x,
  y,
  camera,
  meshes,
  container,
}) => {
  const raymouse = new THREE.Vector2(
    (x / container.clientWidth) * 2 - 1,
    -(y / container.clientHeight) * 2 + 1
  );
  const intersect = _getIntersect({ raymouse, camera, meshes });
  if (!intersect) {
    return {
      intersect
    }
  }
  const mesh = intersect.object;
  const geometry = mesh.geometry;
  // 高速化のため、逆行列をかけておく
  const center = intersect.point
    .clone()
    .applyMatrix4(new THREE.Matrix4().getInverse(mesh.matrix));
//  const scale = mesh.scale.x; // scale.x, scale.y, scale.z are the same
//  const limit = (radius * radius) / (scale * scale);
//  const direction = getRay({ raymouse, camera });
  const geometryState = getGeometryState(geometry);
  const ids = geometryState.getPaintID( center );
  return ids;
};
///////////////////////////////



export const getCurrentParams = ({ meshes }) => {
  let area = 0;
  const areas = {};
  meshes.forEach(mesh => {
    const geometry = mesh.geometry;
    if (!geometry.isBufferGeometry) {
      return;
    }
    const geometryState = getGeometryState(geometry);
    const result = geometryState.getCurrentParams();
    area += result.area;
    result.areas.forEach(o => {
      areas[o.colorId] = (areas[o.colorId] || 0) + o.area;
    });
  });
  return {
    area,
    areas,
  };
};

export const setColorOptions = (options, { meshes }) => {
  meshes.forEach(mesh => {
    const geometry = mesh.geometry;
    if (!geometry.isBufferGeometry) {
      return;
    }
    const geometryState = getGeometryState(geometry);
    geometryState.setColorOptions(options);
  });
};

export const getChanges = ({ meshes }) => {
  const response = {};
  meshes.forEach(mesh => {
    const geometry = mesh.geometry;
    if (!geometry.isBufferGeometry) {
      return;
    }
    const geometryState = getGeometryState(geometry);
    const changes = geometryState.getChanges();
    if(Object.keys(changes).length > 0) {
      response[mesh.name] = changes;
    }
  });
  return response;
};

export const setAnnotation = ({ mesh, colorId, data }) => {
  const geometry = mesh.geometry;
  const geometryState = getGeometryState(geometry);
  geometryState.setAnnotation(colorId, data);
}