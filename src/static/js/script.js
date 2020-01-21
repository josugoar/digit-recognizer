var cnv = document.getElementById("canvas");
var ctx = cnv.getContext("2d");
var position = { x: 0, y: 0 };
// Resize canvas
function setSize() {
  cnv.width  = window.innerWidth;
  cnv.height = window.innerHeight;
  ctx.clearRect(0, 0, cnv.width, cnv.height);
}
// Locate mouse
function setPosition(event) {
  position.x = event.clientX;
  position.y = event.clientY;
}
// Draw line
function draw(event) {
  if (event.buttons === 1) {
    if (mode === "brush") {
      ctx.lineWidth = 10;
      ctx.globalCompositeOperation="source-over";
    } else {
      ctx.lineWidth = 20;
      ctx.globalCompositeOperation="destination-out";
    }
    ctx.beginPath();
    ctx.lineCap = "round";
    ctx.strokeStyle = "white";
    ctx.moveTo(position.x, position.y);
    setPosition(event);
    ctx.lineTo(position.x, position.y);
    ctx.stroke();
  }
}

var compression_ratio = 10;
// Send post request
function post() {
  $("#loading").fadeIn(500);
  res = [cnv.width / compression_ratio, cnv.height / compression_ratio];
  img = cnv.toDataURL("image/jpeg", 1 / compression_ratio).split(",")[1];
  $.ajax({
    type: "POST",
    contentType: "application/json;charset=utf-8",
    async: true,
    url: "/model/predict/",
    data: JSON.stringify({"image": img, "resolution": res}),
    dataType: "json",
    success: function (ret) {
      console.log("Success");
    },
    error: function () {
      console.log("Error");
    },
    complete: function () {
      $("#loading").fadeOut(500);
    }
  });
}

var mode = "brush";
// Change draw mode
$("#brush, #eraser").on("click", function() {
  if (this.id === "brush") {
    mode = "eraser";
  } else {
    mode = "brush";
  }
  $(this).fadeOut(100);
  $(this).css("animation", "float 0.5s ease-in both");
  $("#" + mode).fadeIn(100);
  $("#" + mode).css("animation", "float 0.5s ease-in reverse both");
});

// Show & hide popup
function pop() {
  if ($("#popup").is(":visible")) {
    $("#popup").fadeOut(500);
    $("#popup-button").css("transform", "rotate(0deg)");
  } else {
    $("#popup").fadeIn(500);
    $("#popup-button").css("transform", "rotate(90deg)");
  }
}
