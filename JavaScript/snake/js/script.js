let gameState = 'start';
let board = document.querySelector('.board');
let snake = document.querySelector('.snake');
let fruit = document.querySelector('.fruit');
let message = document.querySelector('.message')
let score = document.querySelector('.score')
let isMoving = 'up';
let lastDirection = 'none';
let boardSize = 30;
let frameTime = 200;
let x = boardSize/2;
let y = boardSize/2;
let fruitX = 0;
let fruitY = 0;
let scoreCounter = 0;
let tail = new Array();
let oldPos = new Array();

document.addEventListener('keydown', (e) => {
  if (e.key == 'Enter') {
    gameState = 'play';
    message.innerHTML = '';
    snake.style.backgroundColor = '#ffffff'
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

function move(){
  tailAdd();
  switch(isMoving){
    case 'up':
      if (lastDirection == 'down'){y++;} else {y--;lastDirection = isMoving;}break;
    case 'down':
      if (lastDirection == 'up'){y--;} else {y++;lastDirection = isMoving;}break;
    case 'left':
      if (lastDirection == 'right'){x++;} else {x--;lastDirection = isMoving;}break;
    case 'right':
      if (lastDirection == 'left'){x--;} else {x++;lastDirection = isMoving;}break;
  }
  snake.style.gridColumnStart = x;
  snake.style.gridColumnEnd = x;
  snake.style.gridRowStart = y;
  snake.style.gridRowEnd = y;

//wall detection
  if (x > boardSize || y > boardSize || x <= 0 || y <= 0){
    gameState = 'over';
  }

//tail detection
  for (var i=0; i<oldPos.length; i++){
    //console.log("x,y:", x, y);
    //console.log("oldPos:", oldPos[i][0], oldPos[i][1])
    if (oldPos[i][0] == x && oldPos[i][1] == y){
      gameState = 'over';
      //console.log("over");
    }
  }

  var element = tail.pop();
  oldPos.pop();
  //console.log(element);
  element.remove();

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
sleep(frameTime);
}

function resetFruit(){
  fruitX = Math.floor(Math.random() * boardSize);
  fruitY = Math.floor(Math.random() * boardSize);
  if (checkFruit() == true){
    if (fruitY == boardSize && fruitX == boardSize){
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
  oldPos.unshift([x,y]);
  /*for (var i = 0; i < tail.length; i++){
    console.log(tail[i]);
  }*/
}

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);

}
