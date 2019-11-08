var J = J || {};

J.websocket = function(viewer) {

  this._viewer = viewer;

  this._socket = null;

  this.connect();

};

J.websocket.prototype.connect = function() {

  try {

    var host = "ws://"+window.location.hostname+":"+window.location.port+"/ws";
    this._socket = new WebSocket(host);

    this._socket.onopen = this.on_open.bind(this);
    this._socket.onmessage = this.on_message.bind(this);
    this._socket.onclose = this.on_close.bind(this);

  } catch (e) {
    console.log('Websocket connection failed.');
  }

};

J.websocket.prototype.on_open = function() {

  console.log('Established websocket connection.');

};

J.websocket.prototype.on_message = function(m) {

    this._viewer._controller.receive(m);

};

J.websocket.prototype.send = function(m) {

  this._socket.send(m);

};

J.websocket.prototype.on_close = function() {

  console.log('Websocket connection dropped.');

};
