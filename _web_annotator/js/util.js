var util = {};
import { APP } from "./APP";

/**
 * 有効な数値かどうかチェックする。文字列なら数値として有効かチェックする
 *
 * @example
 * isNumeric(1) // true
 * isNumeric(123.456) // true
 * isNumeric(0) // true
 * isNumeric(-123) // true
 * isNumeric("abc") // false
 * isNumeric("123") // true
 * isNumeric("-123") // true
 *
 * @param  {string|number} n チェックする対象の値
 * @return {boolean}
 */
util.isNumeric = function(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};

/**
 * マーカー名として有効かチェック
 * 英数字 [a-zA-Z0-9_-] またはスペースで構成される文字列かどうかチェックする
 *
 * @example
 * isMarkerName('abc') // true
 * isMarkerName('Marker Test 3') // true
 * isMarkerName('マーカー') // false
 *
 * @param  {string} str チェックする対象の文字列
 * @return {boolean}
 */
util.isMarkerName = function(string) {
  return /^(?:[a-zA-Z0-9_-]| )+$/.test(string);
};

APP.disposeNode = function(node){
    if (node instanceof THREE.Mesh)
    {
        if (node.geometry)
        {
            node.geometry.dispose ();
        }

        if (node.material)
        {
            if (node.material instanceof THREE.MeshFaceMaterial)
            {
                $.each (node.material.materials, function (idx, mtrl)
                {
                    if (mtrl.map)               mtrl.map.dispose ();
                    if (mtrl.lightMap)          mtrl.lightMap.dispose ();
                    if (mtrl.bumpMap)           mtrl.bumpMap.dispose ();
                    if (mtrl.normalMap)         mtrl.normalMap.dispose ();
                    if (mtrl.specularMap)       mtrl.specularMap.dispose ();
                    if (mtrl.envMap)            mtrl.envMap.dispose ();
                    if (mtrl.alphaMap)          mtrl.alphaMap.dispose();
                    if (mtrl.aoMap)             mtrl.aoMap.dispose();
                    if (mtrl.displacementMap)   mtrl.displacementMap.dispose();
                    if (mtrl.emissiveMap)       mtrl.emissiveMap.dispose();
                    if (mtrl.gradientMap)       mtrl.gradientMap.dispose();
                    if (mtrl.metalnessMap)      mtrl.metalnessMap.dispose();
                    if (mtrl.roughnessMap)      mtrl.roughnessMap.dispose();

                    mtrl.dispose ();    // disposes any programs associated with the material
                });
            }
            else
            {
                if (node.material.map)              node.material.map.dispose ();
                if (node.material.lightMap)         node.material.lightMap.dispose ();
                if (node.material.bumpMap)          node.material.bumpMap.dispose ();
                if (node.material.normalMap)        node.material.normalMap.dispose ();
                if (node.material.specularMap)      node.material.specularMap.dispose ();
                if (node.material.envMap)           node.material.envMap.dispose ();
                if (node.material.alphaMap)         node.material.alphaMap.dispose();
                if (node.material.aoMap)            node.material.aoMap.dispose();
                if (node.material.displacementMap)  node.material.displacementMap.dispose();
                if (node.material.emissiveMap)      node.material.emissiveMap.dispose();
                if (node.material.gradientMap)      node.material.gradientMap.dispose();
                if (node.material.metalnessMap)     node.material.metalnessMap.dispose();
                if (node.material.roughnessMap)     node.material.roughnessMap.dispose();

                node.material.dispose ();   // disposes any programs associated with the material
            }
        }
    }
}   // disposeNode


APP.disposeHierarchy = function(node, callback) {
    for (var i = node.children.length - 1; i >= 0; i--)
    {
        var child = node.children[i];
        disposeHierarchy (child, callback);
        callback (child);
    }
}


