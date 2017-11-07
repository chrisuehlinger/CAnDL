!function init() {
  // create websocket instance
  var socket = new WebSocket("wss://antikythera.local:8080/projector-socket");
  // add event listener reacting when message is received
  socket.onmessage = function (event) {
    let data = JSON.parse(event.data);
    console.log('MESSAGE', data);
    if (data){
      updateModules(data);
    }
  };

  let canvas = document.getElementById('output'),
    ctx = canvas.getContext('2d');

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  let moduleDefintions = [
    {
      name: 'test1',
      preTransform: true,
      onCreate: function (liveModules) {
        console.log('CREATED!');
      },
      onRender: function (ctx, liveModules) {
        let { points, width, height } = this.dimensions;
        ctx.strokeStyle = '#f00';
        ctx.fillStyle = '#0f0';
        ctx.beginPath();
        // ctx.moveTo(points[0][0], points[0][1]);
        // ctx.lineTo(points[1][0], points[1][1]);
        // ctx.lineTo(points[2][0], points[2][1]);
        // ctx.lineTo(points[3][0], points[3][1]);
        ctx.moveTo(0, 0);
        ctx.lineTo(width, 0);
        ctx.lineTo(width, height);
        ctx.lineTo(0, height);
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
        ctx.fillStyle = '#f00';
        ctx.fillText(this.name,0,0);
      },
      onDestroy: function () {
        console.log('DESTROYED!');
      }
    },
    {
      name: 'test3',
      preTransform: true,
      onCreate: function (liveModules) {
        this.startTime = Date.now();
      },
      onRender: function (ctx, liveModules) {
        let { width, height } = this.dimensions,
            progress = ((Date.now()-this.startTime)%1000)/1000;
        ctx.strokeStyle = '#00f';
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(width, 0);
        ctx.lineTo(width, height);
        ctx.lineTo(0, height);
        ctx.closePath();
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, progress*height);
        ctx.lineTo(width, progress*height);
        ctx.stroke();

        ctx.fillStyle = '#f00';
        ctx.fillText(this.name,0,0);
      },
      onDestroy: function () {
        console.log('DESTROYED!');
      }
    },
    {
      name: 'test4',
      preTransform: false,
      onCreate: function (liveModules) {
        console.log('CREATED!');
      },
      onRender: function (ctx, liveModules) {
        let { points, center} = this.dimensions;
        ctx.strokeStyle = '#f00';
        ctx.beginPath();
        ctx.moveTo(points[0][0], points[0][1]);
        ctx.lineTo(points[1][0], points[1][1]);
        ctx.lineTo(points[2][0], points[2][1]);
        ctx.lineTo(points[3][0], points[3][1]);
        ctx.closePath();
        ctx.stroke();

        liveModules.map(mod => {
          if(mod.name === this.name){
            return;
          }
          ctx.beginPath();
          ctx.moveTo(center[0], center[1]);
          ctx.lineTo(mod.dimensions.center[0], mod.dimensions.center[1]);
          ctx.stroke();
        });

        ctx.fillStyle = '#f00';
        ctx.fillText(this.name, center[0], center[1]);
      },
      onDestroy: function () {
        console.log('DESTROYED!');
      }
    },
  ];

  let liveModules = [];
  //updateModules();

  function updateModules(newModules) {

    console.log('updateModules start', newModules);

    let brandNewModules = newModules.filter(newModule => !liveModules.reduce((isLive, liveModule) => isLive || liveModule.name === newModule.name, false)),
        missingModules = liveModules.filter(liveModule => !newModules.reduce((isStillLive, newModule) => isStillLive || liveModule.name === newModule.name, false)),
        stillThereModules = liveModules.filter(liveModule => newModules.reduce((isStillLive, newModule) => isStillLive || liveModule.name === newModule.name, false)),
        newlyInstantiatedModules = [],
        modulesToDestroy = [];

        brandNewModules.map(newModuleFrame => {
          // TODO: Instantiate any newModules that weren't there before
          let newModuleDefinition = moduleDefintions.filter(moduleDef => moduleDef.name === newModuleFrame.name)[0],
              { points } = newModuleFrame,
              newModule = Object.assign({
                dimensions: {
                  points,
                  center: points.reduce((center,point) => [center[0] + point[0]/4, center[1] + point[1]/4], [0,0]),
                  width: Math.sqrt((points[1][1] - points[0][1])**2 + (points[1][0] - points[0][0])**2),
                  height: Math.sqrt((points[3][1] - points[0][1])**2 + (points[3][0] - points[0][0])**2),
                  rotation: Math.atan2(points[1][1]-points[0][1], points[1][0]-points[0][0])
                },
                missingCount: 0
              }, newModuleDefinition);

          liveModules.push(newModule);
          newlyInstantiatedModules.push(newModule);
        });

        stillThereModules.map(stillThereModule => {
          let newModuleFrame = newModules.filter(newModule => newModule.name === stillThereModule.name)[0],
              { points } = newModuleFrame;

          stillThereModule.dimensions = {
            points,
            center: points.reduce((center,point) => [center[0] + point[0]/4, center[1] + point[1]/4], [0,0]),
            width: Math.sqrt((points[1][1] - points[0][1])**2 + (points[1][0] - points[0][0])**2),
            height: Math.sqrt((points[3][1] - points[0][1])**2 + (points[3][0] - points[0][0])**2),
            rotation: Math.atan2(points[1][1]-points[0][1], points[1][0]-points[0][0])
          };
          stillThereModule.missingCount = 0;
        });

        missingModules.map(missingModule => {
          missingModule.missingCount++;
          if(missingModule.missingCount >= 3) {
            missingModule.onDestroy(liveModules);
            modulesToDestroy.push(missingModule);
          }
        });

        // console.log('updateModules beforeFinish:', {
        //   newModules,
        //   brandNewModules,
        //   missingModules,
        //   stillThereModules,
        //   liveModules,
        //   newlyInstantiatedModules,
        //   modulesToDestroy
        // });

        liveModules = liveModules.filter(liveModule => !modulesToDestroy.reduce((foundMatch, modToDestroy) => foundMatch || modToDestroy.name === liveModule.name, false));

        newlyInstantiatedModules.map(newMod => newMod.onCreate(liveModules));
  }

  !function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    liveModules.map(liveModule => {
      let { points, rotation} = liveModule.dimensions;

      ctx.save();
      if(liveModule.preTransform){
        ctx.translate(points[0][0], points[0][1]);
        ctx.rotate(rotation);
      }
      liveModule.onRender(ctx, liveModules);
      ctx.restore();
    });
    requestAnimationFrame(render);
  }()

}()
