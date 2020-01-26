var cnvs = document.getElementsByTagName("canvas");
var rndr_ctx = cnvs[0].getContext("2d");
var skct_ctx = cnvs[1].getContext("2d");
var position = { x: 0, y: 0 };
// Resize canvas
function setSize(cnvs) {
  for (let i = 0; i < cnvs.length; i++) {
    cnvs[i].width = window.innerWidth;
    cnvs[i].height = window.innerHeight;
    cnvs[i].getContext("2d").clearRect(0, 0, cnvs[i].width, cnvs[i].height);
  }
}
// Locate mouse
function setPosition(event) {
  position.x = event.clientX;
  position.y = event.clientY;
}
// Draw line
function draw(event) {
  if ($("strong").is(":visible")) {
    $("strong").fadeOut(250);
  }
  if (event.buttons === 1) {
    if (mode === "brush") {
      skct_ctx.lineWidth = 10;
      skct_ctx.globalCompositeOperation="source-over";
    } else {
      skct_ctx.lineWidth = 20;
      skct_ctx.globalCompositeOperation="destination-out";
    }
    skct_ctx.beginPath();
    skct_ctx.lineCap = "round";
    skct_ctx.strokeStyle = "white";
    skct_ctx.moveTo(position.x, position.y);
    setPosition(event);
    skct_ctx.lineTo(position.x, position.y);
    skct_ctx.stroke();
  }
}

var compression_ratio = 10;
// Send post request
function post() {
  $(".load-wrapper").fadeIn(500);
  img = cnvs[1].toDataURL("image/jpeg", 1 / compression_ratio).split(",")[1];
  $.ajax({
    type: "POST",
    contentType: "application/json;charset=utf-8",
    async: true,
    url: "/model/predict/",
    data: JSON.stringify({
      "image": img,
      "show": true,
      "save": false
    }),
    dataType: "json",
    success: function (ret) {
      console.log(ret);
      if (ret) {
        for (let i = 0; i < ret.length; i++) {
          rndr_ctx.lineWidth = 3;
          rndr_ctx.strokeStyle = "black";
          rndr_ctx.beginPath();
          rndr_ctx.rect(ret[i].x, ret[i].y, ret[i].width, ret[i].height);
          rndr_ctx.stroke();
          rndr_ctx.font = "30px Arial";
          rndr_ctx.fillText(ret[i].pred, ret[i].x, ret[i].y - 5);
        }
      }
    },
    error: function () {
      console.log("Error");
    },
    complete: function () {
      $(".load-wrapper").fadeOut(500);
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
  if ($(".popup-wrapper").is(":visible")) {
    $(".popup-wrapper").fadeOut(500);
    $(".popup-button").css("transform", "rotate(0deg)");
  } else {
    $(".popup-wrapper").fadeIn(500);
    $(".popup-button").css("transform", "rotate(90deg)");
  }
}
