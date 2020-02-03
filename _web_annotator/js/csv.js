// TabulatorのcsvFormatterに不具合があるため再定義する
// csvFormatter from Download.prototype.downloaders in tabulator.js
export const csvFormatter = function(columns, data, options, setFileContents, config) {
  // TabulatorのcsvFormatterは隠れてるカラムがダウンロード対象にならないためカラムを再定義する
  var columnDefinitions = this.table.getColumnDefinitions();
  columns = columnDefinitions.filter(function(column) {
    return column.download !== false;
  });

  var self = this,
    titles = [],
    fields = [],
    delimiter = options && options.delimiter ? options.delimiter : ",",
    fileContents;

  //build column headers
  function parseSimpleTitles() {
    columns.forEach(function (column) {
      titles.push('"' + String(column.title).split('"').join('""') + '"');
      fields.push(column.field);
    });
  }

  function parseColumnGroup(column, level) {
    if (column.subGroups) {
      column.subGroups.forEach(function (subGroup) {
        parseColumnGroup(subGroup, level + 1);
      });
    } else {
      titles.push('"' + String(column.title).split('"').join('""') + '"');
      fields.push(column.definition.field);
    }
  }

  if (config.columnGroups) {
    console.warn("Download Warning - CSV downloader cannot process column groups");
    columns.forEach(function (column) {
      parseColumnGroup(column, 0);
    });
  } else {
    parseSimpleTitles();
  }

  //generate header row
  fileContents = [titles.join(delimiter)];

  function parseRows({ data }) {
    //generate each row of the table
    data.forEach(function (row) {
      var rowData = [];

      fields.forEach(function(field) {
        // getFieldValueを使うと数値がfalseになるため単純にrowの値を使う
        //var value = self.getFieldValue(field, row);
        var value = row[field];

        switch (typeof value) {
          case "object":
            value = JSON.stringify(value);
            break;
          case "undefined":
          case "null":
            value = "";
            break;
        }

        //escape quotation marks
        rowData.push('"' + String(value).split('"').join('""') + '"');
      });

      fileContents.push(rowData.join(delimiter));
    });
  }

  function parseGroup(group) {
    if (group.subGroups) {
      group.subGroups.forEach(function (subGroup) {
        parseGroup(subGroup);
      });
    } else {
      parseRows(group.rows);
    }
  }

  if (config.rowGroups) {
    console.warn("Download Warning - CSV downloader cannot process row groups");
    data.forEach(function (group) {
      parseGroup(group);
    });
  } else {
    parseRows(data);
  }

  setFileContents(fileContents.join("\n"), "text/csv");
};


/**
 * カンマ区切りのCSV文字列から配列に変換する
 *
 * @param  {string} csv カンマ区切りの文字列
 * @return {Array}  変換した配列
 */
export function parseCSV(csv) {
  var result = [];
  var array = csv2array(csv);

  for (var i = 1; i < array.length; i++) {
    result[i - 1] = {};
    for (var k = 0; k < array[0].length && k < array[i].length; k++) {
      var key = array[0][k];
      result[i - 1][key] = array[i][k];
    }
  }

  return result;
}

/**
 * カンマ区切りCSVの一行を配列に変換する
 *
 * 参考: RFC4180 - Common Format and MIME Type for Comma-Separated Values (CSV) Files
 * https://tools.ietf.org/html/rfc4180
 * https://stackoverflow.com/questions/33155999/converting-a-csv-file-into-a-2d-array/33156233
 *
 * @param  {string} csv カンマ区切りの文字列
 * @param  {string} [delimiter=','] 区切り文字。デフォルト=','
 * @return {array} カンマ区切りをを変換した配列
 */
function csv2array(csv, delimiter) {
  delimiter = delimiter || ',';

  var pattern = new RegExp(
    // [1] delimiter
    '(\\' + delimiter + '|\\r?\\n|\\r|^)' +
    '(?:' +
      // [2] quoted value
      '"([^"]*(?:""[^"]*)*)"|' +
      // [3] standard value
      '([^"\\' + delimiter + '\\r\\n]*)'+
    ')',
    'gi'
  );

  var array = [[]];
  var m, matchedDelimiter, matchedValue;

  while ((m = pattern.exec(csv))) {
    matchedDelimiter = m[1];
    if (matchedDelimiter.length && matchedDelimiter !== delimiter) {
      array.push([]);
    }

    if (m[2]) {
      matchedValue = m[2].replace(/""/g, '"');
    } else {
      matchedValue= m[3];
    }
    array[array.length - 1].push(matchedValue);
  }

  return array;
}
