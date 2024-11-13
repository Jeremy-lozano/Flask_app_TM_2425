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
  const form = $('#dynamicForm');
  const nomValue = $('#nomInput').val();
  const newDiv = $(`
    <div class="form-group">
      <label>${nomValue} :</label>
      <input type="text" name="quantite[]" id="form"placeholder="Quantité">
    </div>
  `);

  form.find('.add-button').before(newDiv);
  $('#nomInput').val('');
}

$(function() {
  $('#nomInput').on('input', function() {
    const query = $(this).val();
    if (query.length > 1) {
      console.log("Recherche de suggestions pour :", query);
      $.ajax({
        url: `${window.location.origin}/recette/suggestions`,
        type: 'GET',
        data: { q: query },
        success: function(data) {
          console.log("Données reçues :", data);
          const suggestionsList = $('#suggestionsList').empty();
          if (data.length) {
            data.forEach(item => {
              suggestionsList.append(
                `<div class="suggestion-item" onclick="selectSuggestion(${item.id_ingredient}, '${item.nom}')">${item.nom}</div>`
              );
            });
          }
        },
        error: function(xhr, status, error) {
          console.error("Erreur AJAX:", error);
        }
      });
    } else {
      $('#suggestionsList').empty();
    }
  });
});

function selectSuggestion(id_ingredient, nom) {
  $('#nomInput').val(nom);
  $('#suggestionsList').empty();
  addIngredientToList(id_ingredient, nom);
}

function addIngredientToList(id_ingredient, nom) {
  const ingredientElement = `
    <div class="ingredient-item" data-id_ingredient="${id_ingredient}">
      <span>${nom}</span>
      <input type="number" class="quantity-input" name="quantite[]" placeholder="Quantité" />
    </div>
  `;
  $('#ingredientsList').append(ingredientElement);
}
