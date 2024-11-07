console.log("Script bien chargé")

function previewImage(event) {
    const reader = new FileReader();
    
    const fileName = event.target.files[0].name;
  const fileNameElement = document.getElementById('fileName');
  fileNameElement.textContent = fileName;
  fileNameElement.style.display = 'block'; // Rendre visible le nom du fichier
  
  // Lire le fichier sélectionné
  reader.readAsDataURL(event.target.files[0]);
}


function increase_nbr_personne() { 
  var nombre_personne = document.getElementById('nombre_personne'); 
  nombre_personne.value = parseInt(nombre_personne.value) + 1; 
} 
function decrease_nbr_personne() { 
    var nombre_personne = document.getElementById('nombre_personne'); 
    if (nombre_personne.value > 1) 
      { nombre_personne.value = parseInt(nombre_personne.value) - 1; } 
}


function adjust_temps_preparation(action) {
  var temps_preparation = document.getElementById('temps_preparation');
  var currentValue = temps_preparation.value;
  var totalMinutes = 0;  // récupérer les donnée du champs "temps_preparation"

  // Convertir l'affichage actuel en minutes totales
  if (currentValue.includes('heure')) {
      var parts = currentValue.split(' ');
      var hours = parseInt(parts[0]) || 0;
      var minutes = parts.length > 2 ? parseInt(parts[2]) || 0 : 0;
      totalMinutes = (hours * 60) + minutes;
  } else {
      totalMinutes = parseInt(currentValue) || 0;
  }

  // Ajuster les minutes selon l'action (augmenter ou diminuer)
  totalMinutes += (action === 'increase') ? 15 : -15;

  // Assurer que le total des minutes ne devienne pas négatif
  totalMinutes = Math.max(totalMinutes, 0);

  // Mettre à jour l'affichage selon le total des minutes
  if (totalMinutes >= 60) {
      var hours = Math.floor(totalMinutes / 60);
      var remainingMinutes = totalMinutes % 60;
      temps_preparation.value = hours + ' heure' + (hours > 1 ? 's' : '') + (remainingMinutes > 0 ? ' ' + remainingMinutes + ' minutes' : '');
  } else {
      temps_preparation.value = totalMinutes + ' minutes';
  }
}

// Fonctions pour augmenter et diminuer le temps de préparation
function increase_temps_preparation() {
  adjust_temps_preparation('increase');
}

function decrease_temps_preparation() {
  adjust_temps_preparation('decrease');
}

function adjust_temps_cuisson(action) {
  var temps_preparation = document.getElementById('temps_cuisson');
  var currentValue = temps_preparation.value;
  var totalMinutes = 0;  // récupérer les donnée du champs "temps_cuisson"

  // Convertir l'affichage actuel en minutes totales
  if (currentValue.includes('heure')) {
      var parts = currentValue.split(' ');
      var hours = parseInt(parts[0]) || 0;
      var minutes = parts.length > 2 ? parseInt(parts[2]) || 0 : 0;
      totalMinutes = (hours * 60) + minutes;
  } else {
      totalMinutes = parseInt(currentValue) || 0;
  }

  // Ajuster les minutes selon l'action (augmenter ou diminuer)
  totalMinutes += (action === 'increase') ? 15 : -15;

  // Assurer que le total des minutes ne devienne pas négatif
  totalMinutes = Math.max(totalMinutes, 0);

  // Mettre à jour l'affichage selon le total des minutes
  if (totalMinutes >= 60) {
      var hours = Math.floor(totalMinutes / 60);
      var remainingMinutes = totalMinutes % 60;
      temps_preparation.value = hours + ' heure' + (hours > 1 ? 's' : '') + (remainingMinutes > 0 ? ' ' + remainingMinutes + ' minutes' : '');
  } else {
      temps_preparation.value = totalMinutes + ' minutes';
  }
}

// Fonctions pour augmenter et diminuer le temps de préparation
function increase_temps_cuisson() {
  adjust_temps_cuisson('increase');
}

function decrease_temps_cuisson() {
  adjust_temps_cuisson('decrease');
}



function addNomQuantite() {
  // Sélectionner le formulaire dynamique
  var form = document.getElementById('dynamicForm');

  // Récupérer la valeur saisie dans le champ "Nom"
  var nomValue = document.getElementById('nomInput').value;

  // Créer une nouvelle div pour la nouvelle ligne de formulaire
  var newDiv = document.createElement('div');
  newDiv.className = 'form-group';

  // Ajouter le nom saisi suivi d'un champ pour la quantité
  newDiv.innerHTML = `<label>${nomValue} :</label> <input id='form' type="text" name="quantite[]" placeholder="Quantité">`;

  //trouver le bouton ajouter
  var addButton = form.querySelector('.add-button');
  // Ajouter la nouvelle div au formulaire
  form.insertBefore(newDiv, addButton);

  // Réinitialiser le champ "Nom"
  document.getElementById('nomInput').value = '';
}