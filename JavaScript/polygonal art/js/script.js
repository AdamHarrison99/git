var sizeSlider = document.querySelector(".sizeSlider");
var complexitySlider = document.querySelector(".complexitySlider");
var colorSlider = document.querySelector(".colorSlider");
var sizeVal = document.getElementById("sizeValueNum");
var complexityVal = document.getElementById("complexityValueNum");
var colorVal = document.getElementById("colorValueNum");
var imageCanvas = document.getElementById("image")

sizeVal.innerHTML = sizeSlider.value;
complexityVal.innerHTML = complexitySlider.value;
colorVal.innerHTML = colorSlider.value;

sizeSlider.oninput = function() {
  sizeVal.innerHTML = sizeSlider.value;
}

complexitySlider.oninput = function() {
  complexityVal.innerHTML = complexitySlider.value;
}

colorSlider.oninput = function() {
  colorVal.innerHTML = colorSlider.value;
}

var loadImage = function(event){
  var imageUpload = document.getElementById("file-upload");
  imageCanvas.src = URL.createObjectURL(event.target.files[0]);
}

function save(event){
  return 0;
}

function reset(event){
  location.reload();
}
