var sizeSlider = document.querySelector(".sizeSlider");
var complexitySlider = document.querySelector(".complexitySlider");
var colorSlider = document.querySelector(".colorSlider");
var sizeVal = document.getElementById("sizeValueNum");
var complexityVal = document.getElementById("complexityValueNum");
var colorVal = document.getElementById("colorValueNum");
var imageCanvas = document.getElementById("image")
var board = document.querySelector(".board");
var randColors = [];

var colorGenerator = function (path) { //TODO randomness from colorSlider.value as seed. Lower colorSlider.value = less color change. Higher colorSlider.value = large color change between polygons
  if (randColors.length < colorSlider.value){
    randColors.push('#'+ ("00000" + Math.floor(Math.random() * Math.pow(16, 6)).toString(16)).slice(-6));
    colorGenerator();
  }
  if (randColors.length > colorSlider.value){
    randColors.pop();
    colorGenerator();
  }

  return (randColors[Math.floor(Math.random()*randColors.length).toString(16)]);
};

sizeVal.innerHTML = sizeSlider.value;
complexityVal.innerHTML = complexitySlider.value;
colorVal.innerHTML = colorSlider.value;
var mySVG = new Triangulr (500, 500, Number(sizeSlider.value), Number(complexitySlider.value), colorGenerator);
board.appendChild(mySVG);

sizeSlider.oninput = function() {
  sizeVal.innerHTML = sizeSlider.value;
  optionsUpdate()
}

complexitySlider.oninput = function() {
  complexityVal.innerHTML = complexitySlider.value;
  optionsUpdate()
}

colorSlider.oninput = function() {
  colorVal.innerHTML = colorSlider.value;
  optionsUpdate()
}

function optionsUpdate(){
  board.removeChild(board.firstElementChild);
  var mySVG = new Triangulr (500, 500, Number(sizeSlider.value), Number(complexitySlider.value), colorGenerator);
  board.appendChild(mySVG);
}

var loadImage = function(event){
  var imageUpload = document.getElementById("file-upload");
  imageCanvas.src = URL.createObjectURL(event.target.files[0]);
}

window.addEventListener("resize", function(event) {
  console.log(document.body.clientWidth + ' wide by ' + document.body.clientHeight+' high');
})

function save(event){
  return 0;
}

function reset(event){
  location.reload();
}
