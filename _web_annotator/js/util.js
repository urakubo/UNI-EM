var util = {};

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
