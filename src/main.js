// create websocket instance
var socket = new WebSocket("ws://localhost:8080/ws");
// add event listener reacting when message is received
socket.onmessage = function (event) {
  let data = JSON.parse(event.data);
  console.log('MESSAGE', data);
  render(data);
};

let canvas = document.getElementById('output'),
    ctx = canvas.getContext('2d');

function render(newFrame){
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  newFrame.forEach(function(rect){
    ctx.strokeStyle = '#f00';
    ctx.fillStyle = '#0f0';
    ctx.beginPath();
    ctx.moveTo(rect[0][0],rect[0][1]);
    ctx.lineTo(rect[1][0],rect[1][1]);
    ctx.lineTo(rect[2][0],rect[2][1]);
    ctx.lineTo(rect[3][0],rect[3][1]);
    ctx.closePath();
    ctx.stroke();
    ctx.fill();
  });
}
