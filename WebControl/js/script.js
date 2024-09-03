
// Fonction pour mettre à jour l'angle de rotation de l'aiguille en fonction de la vitesse
function updateRotation(speed) {
  const minSpeed = 0; // Vitesse minimale en km/h
  const maxSpeed = 120; // Vitesse maximale en km/h
  const minAngle = -130; // Angle minimal de l'aiguille
  const maxAngle = 138; // Angle maximal de l'aiguille (correspondant à la vitesse maximale)
  // Limiter la vitesse et angle minimale
  speed = Math.max(minSpeed, speed);
  // Limiter la vitesse et angle  maximale
  speed = Math.min(maxSpeed, speed);
  // Calcul de l'angle en fonction de la vitesse
  var angle = (speed / maxSpeed) * maxAngle;
  angle = Math.max(minAngle, angle);
  angle = Math.min(maxAngle, angle);
  // Mise à jour de l'aiguille avec le nouvel angle
  // Calculer la rotation en fonction de l'angle et de la direction
  let rotation = (angle + 112) * 1.923; // Convertir l'angle en rotation (360/242)
  // Mise à jour de l'aiguille
  const pointer = document.getElementById("pointer");
  pointer.style.transform = `translateX(-50%) rotate(${rotation}deg)`;
}

$(function () {
  var isTouchDevice = "ontouchstart" in document.documentElement ? true : false;
  var BUTTON_DOWN = isTouchDevice ? "touchstart" : "mousedown";
  var BUTTON_UP = isTouchDevice ? "touchend" : "mouseup";

  $("button").bind(BUTTON_DOWN, function () {
    $(this).addClass("btn-pressed");
    $.post("/cmd", this.id, function (data, status) {});
  });

  $("button").bind(BUTTON_UP, function () {
    $(this).removeClass("btn-pressed");
    $.post("/cmd", "stop", function (data, status) {});
  });

  $("input").change(function () {
    var speed = this.value;
    const counter = document.getElementById("counter");
    $("#speed-display").text(speed); // Met à jour l'élément HTML avec l'id 'speed-display' avec la nouvelle valeur
    updateRotation(speed); // Met à jour l'aiguille avec la nouvelle vitesse
    // Ajouter des zéros devant la vitesse si elle est inférieure à 100
    const formattedSpeed = ("000" + speed).slice(-3);
    counter.textContent = formattedSpeed;    $.post("/cmd", { speed: speed }); // Envoie la nouvelle valeur de vitesse au serveur
  });

  // Positionner l'aiguille à la valeur 50 lors de l'initialisation
  updateRotation(30);
});

$(function () {
  var isTouchDevice = "ontouchstart" in document.documentElement ? true : false;
  var BUTTON_DOWN = isTouchDevice ? "touchstart" : "mousedown";
  var BUTTON_UP = isTouchDevice ? "touchend" : "mouseup";

  $("input[type='checkbox']").change(function () {
    var id = this.id;
    if (this.checked) {
      $.post("/cmd", id, function (data, status) {});
    } else {
      $.post("/cmd", "stop", function (data, status) {});
    }
  });

  $('input[type="range"]').change(function () {
    var speed = this.value;
    $.post("/cmd", { speed: speed });
  });
});

function confirmReboot() {
  if (confirm("Êtes-vous sûr de vouloir redémarrer le Raspberry Pi ?")) {
    document.getElementById("rebootForm").submit();
  }
}