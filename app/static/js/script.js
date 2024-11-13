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

$(document).ready(function() {
  // Gestion de l'input pour la recherche d'ingrédients
  $('#nomInput').on('input', function() {
      var query = $(this).val();  // Déclare la variable 'query' ici pour récupérer la valeur de l'input

      if (query.length > 1) {  // Si l'utilisateur tape plus de 1 caractère
          console.log("Recherche de suggestions pour :", query);

          // Effectuer la requête AJAX pour récupérer les suggestions d'ingrédients
          $.ajax({
              url: window.location.origin + '/recette/suggestions',  // URL avec le préfixe '/recette'
              type: 'GET',
              data: { q: query },  // Envoie le paramètre 'q' avec la valeur de l'input
              success: function(data) {
                  console.log("Données reçues :", data);
                  $('#suggestionsList').empty();  // Vide la liste des suggestions

                  // Si des résultats sont trouvés, les afficher dans la liste
                  if (data.length) {
                      data.forEach(item => {
                          // Ajoute chaque suggestion à la liste sous forme de div cliquable
                          $('#suggestionsList').append(
                              `<div class="suggestion-item" onclick="selectSuggestion(${item.id}, '${item.nom}')">${item.nom}</div>`
                          );
                      });
                  }
              },
              error: function(xhr, status, error) {
                  console.error("Erreur AJAX:", error);  // Si une erreur se produit
              }
          });
      } else {
          $('#suggestionsList').empty();  // Si moins de 2 caractères, on vide la liste
      }
  });
});

// Fonction qui est appelée lorsqu'une suggestion est sélectionnée
function selectSuggestion(id, nom) {
  $('#nomInput').val(nom);  // Place le nom de l'ingrédient dans le champ de saisie
  $('#suggestionsList').empty();  // Vide la liste des suggestions

  // Ajouter l'ingrédient sélectionné à la liste des ingrédients en bas du formulaire
  // (Supposons que tu as une fonction `addIngredientToList` pour l'ajouter)
  addIngredientToList(id, nom);
}

// Fonction pour ajouter l'ingrédient sélectionné à la liste (ou autre logique spécifique)
function addIngredientToList(id, nom) {
  const ingredientElement = `
      <div class="ingredient-item" data-id="${id}">
          <span>${nom}</span>
          <input type="number" class="quantity-input" placeholder="Quantité" />
      </div>
  `;
  $('#ingredientsList').append(ingredientElement);  // Ajoute l'élément au conteneur
}



