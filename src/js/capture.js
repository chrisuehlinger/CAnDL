!function init() {
  let canvas = document.createElement('canvas'),
    context = canvas.getContext('2d'),
    video = document.querySelector('video');

  navigator.mediaDevices.getUserMedia({ audio: false, video: { facingMode: "environment" } })
    .then(function (stream) {
      /* use the stream */
      console.log('GOTIT', stream);
      video.srcObject = stream;
      video.addEventListener('click', takeSnapshot);

      let socket = new WebSocket("ws://antikythera.local:8080/capture-socket");
      // add event listener reacting when message is received
      socket.onmessage = function (event) {
        console.log('CAPTURE');
        let data = takeSnapshot;
        socket.send(data);
      };

      function takeSnapshot() {
        var context,
          width = video.offsetWidth,
          height = video.offsetHeight;
        canvas.width = width;
        canvas.height = height;

        context.drawImage(video, 0, 0, width, height);

        return canvas.toDataURL('image/png');
      }


    })
    .catch(function (err) {
      /* handle the error */
      throw err;
    });

}()
