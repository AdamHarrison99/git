let gameState = 'start';
let board = document.querySelector('.board');
let snake = document.querySelector('.snake');
let fruit = document.querySelector('.fruit');
let message = document.querySelector('.message')
let score = document.querySelector('.score')
let isMoving = 'up';
let x = 25;
let y = 25;
let fruitX = 5;
let fruitY = 5;
let scoreCounter = 0;
let tail = new Array();

document.addEventListener('keydown', (e) => {
  if (e.key == 'Enter') {
    gameState = 'play'
    message.innerHTML = '';

    fruit.style.backgroundColor = '#7CFC00';

    //controls.style.visibility = "hidden";
    requestAnimationFrame(() => {resetFruit(); game();});
  }
  if (gameState == 'play') {
    if (e.key == 'w') {
      isMoving = 'up';
    }
    if (e.key == 's') {
      isMoving = 'down';
    }
    if (e.key == 'a') {
      isMoving = 'left';
    }
    if (e.key == 'd') {
      isMoving = 'right';
    }
  }
});

function move(){ //TODO dont let player go backwards
  tailAdd();
  switch(isMoving){
    case 'up':
      y--;
      snake.style.gridColumnStart = x;
      snake.style.gridColumnEnd = x;
      snake.style.gridRowStart = y;
      snake.style.gridRowEnd = y;
      break;
    case 'down':
      y++;
      snake.style.gridColumnStart = x;
      snake.style.gridColumnEnd = x;
      snake.style.gridRowStart = y;
      snake.style.gridRowEnd = y;
      break;
    case 'left':
      x--;
      snake.style.gridColumnStart = x;
      snake.style.gridColumnEnd = x;
      snake.style.gridRowStart = y;
      snake.style.gridRowEnd = y;
      break;
    case 'right':
      x++;
      snake.style.gridColumnStart = x;
      snake.style.gridColumnEnd = x;
      snake.style.gridRowStart = y;
      snake.style.gridRowEnd = y;
      break;
  }
  var element = tail.pop();
  //console.log(element);
  element.remove();

  if (x > 50 || y > 50 || x <= 0 || y <= 0){
    gameState = 'over';
  }
  requestAnimationFrame(() => {game();});
}

function game(){
if (gameState == 'over'){
  message.innerHTML = "Game Over<br>Score: " + scoreCounter;
  return;
}
if (checkFruit() == true){
  updateScore();
  resetFruit();
}
move();
tailCollisionDetection();
sleep(300);
}

function resetFruit(){
  fruitX = Math.floor(Math.random() * 50);
  fruitY = Math.floor(Math.random() * 50);
  if (checkFruit() == true){
    if (fruitY == 50 && fruitX == 50){
      fruitX--;
      fruitY--;
    } else {
      fruitX++;
      fruitY++;
    }
  }

  //console.log(fruitX, fruitY)

  fruit.style.gridColumnStart = fruitX;
  fruit.style.gridColumnEnd = fruitX;
  fruit.style.gridRowStart = fruitY;
  fruit.style.gridRowEnd = fruitY;

}

function checkFruit(){
  if (fruitX == x && fruitY == y){
    return true;
  }
}

function updateScore(){
  scoreCounter++;
  score.innerHTML = scoreCounter;
  tailAdd();
}

function tailAdd(){
  var cell = document.createElement("div");
  board.appendChild(cell);

  cell.style.backgroundColor = '#ffffff'
  cell.style.gridColumnStart = x;
  cell.style.gridColumnEnd = x;
  cell.style.gridRowStart = y;
  cell.style.gridRowEnd = y;

  tail.unshift(cell);
  /*for (var i = 0; i < tail.length; i++){
    console.log(tail[i]);
  }*/
}

function tailCollisionDetection(){ //TODO this
  
}

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);

}
