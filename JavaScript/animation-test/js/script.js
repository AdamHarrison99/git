const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const CANVAS_W = canvas.width = 600;
const CANVAS_H = canvas.height = 600;

const dog = new Image();
dog.src = 'shadow_dog.png';
const spriteW = 575;
const spriteH = 523
let frameX = 0;
let frameY = 0;
let numOfSprites = 6;
let frame = 0;

function nextAnimation(){
  if (frameY < 9){
    frameY++
  } else {frameY = 0}

  switch(frameY){
    case 0: case 1: case 2: case 6: case 7:
      numOfSprites = 6;
      break;
    case 3:
      numOfSprites = 8;
      break;
    case 4:
      numOfSprites = 10;
      break;
    case 5:
      numOfSprites = 4;
      break;
    case 8:
      numOfSprites = 11;
      break;
    case 9:
      numOfSprites = 3;
      break;
    }
console.log(numOfSprites, frameY);
};

function animate(){
  ctx.clearRect(0,0,CANVAS_W,CANVAS_H);
  //ctx.drawImage(image,sx,sy,sw,sh,dx,dy,dw,dh)
  ctx.drawImage(dog,frameX * spriteW,frameY * spriteH,spriteW,spriteH,0,0,spriteW,spriteH);
  if (frame % 5 == 0){
    if (frameX < numOfSprites) frameX++;
    else frameX = 0;
  }

  frame++;
  requestAnimationFrame(animate);
};
animate();
