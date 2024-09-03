$(document).ready(function () {
  function updateTestStatus() {
    $.getJSON("/test_status", function (data) {
      let tableBody = $("#testStatusTable");
      tableBody.empty(); // Vider le tableau avant d'ajouter les nouvelles lignes

      // Parcourir les résultats des tests et ajouter une ligne pour chaque test
      $.each(data, function (test, result) {
        let status = result ? "Réussi" : "Échoué";
        let row = `<tr><td>${test}</td><td>${status}</td></tr>`;
        tableBody.append(row);
      });
    });
  }

  // Mettre à jour l'état des tests toutes les 5 secondes
  setInterval(updateTestStatus, 5000);

  // Appel initial pour charger l'état des tests immédiatement
  updateTestStatus();
});
