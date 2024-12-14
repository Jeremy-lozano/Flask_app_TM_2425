console.log("Script bien chargé")

function previewImage(event) {
  const fileName = event.target.files[0].name;
  const fileNameElement = document.getElementById('fileName');
  fileNameElement.textContent = fileName;
  fileNameElement.style.display = 'block'; // Rendre visible le nom du fichier
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


function addNomQuantite(id_ingredient, nom) {
  const form = $('#dynamicForm');
  const newDiv = $(`
    <div class="form-group">
      <label>${nom} :</label>
      <input type="text" name="quantite[]" placeholder="Quantité">
      <input type="hidden" name="id_ingredient[]" value="${id_ingredient}">
    </div>
  `);

  // Ajouter le nouveau div pour l'ingrédient avec sa quantité
  form.find('.add-button').after(newDiv);
  console.log("Nouvel ingrédient ajouté avec quantité :", {
    nom: nom,
    id_ingredient: id_ingredient
  });

  // Vider la barre de recherche après ajout de l'ingrédient
  $('#nomInput').val('');
}

$(function() {
  // Quand l'utilisateur tape dans la barre de recherche
  $('#nomInput').on('input', function() {
    const query = $(this).val(); // Valeur de la barre de recherche
    if (query.length > 1) {
      console.log("Recherche de suggestions pour :", query);
      $.ajax({
        url: `${window.location.origin}/recette/suggestions`, // URL pour récupérer les suggestions
        type: 'GET',
        data: { q: query },
        success: function(data) {
          console.log("Données reçues :", data);
          const suggestionsList = $('#suggestionsList').empty(); // Vider la liste des suggestions
          if (data.length) {
            // Ajouter chaque suggestion à la liste
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
      $('#suggestionsList').empty(); // Si la barre de recherche est vide, vider la liste des suggestions
    }
  });
});

function selectSuggestion(id_ingredient, nom) {
  // Mettre le nom de l'ingrédient dans la barre de recherche
  $('#nomInput').val(nom);
  
  // Vider la liste des suggestions dès que l'on sélectionne un ingrédient
  $('#suggestionsList').empty();

  console.log("Suggestion sélectionnée :", {
    id_ingredient: id_ingredient,
    nom: nom
  });

  // Ajouter l'ingrédient à la liste
  addIngredientToList(id_ingredient, nom);
}

function addIngredientToList(id_ingredient, nom) {
  // Créer un élément d'ingrédient avec un champ pour la quantité
  const ingredientElement = `
    <div class="ingredient-item" data-id_ingredient="${id_ingredient}">
      <span>${nom}</span>
      <input type="text" class="quantity-input" name="quantite[]" placeholder="Quantité">
      <input type="hidden" name="id_ingredient[]" value="${id_ingredient}">
    </div>
  `;
  
  // Ajouter l'élément à la liste des ingrédients
  $('#ingredientsList').append(ingredientElement);
  console.log("Ingrédient ajouté à la liste :", {
    id_ingredient: id_ingredient,
    nom: nom
  });

  // Après avoir ajouté l'ingrédient, vider la barre de recherche pour un nouvel ajout
  $('#nomInput').val('');
}

  function toggleColor(id, id_utilisateur, id_recette) {
    console.log("ID du bouton : ", id);

    const btn = document.getElementById(id);
    if (!btn) {
        console.error("Élément avec l'ID " + id + " non trouvé dans le DOM.");
        return;  // Sortir de la fonction si l'élément n'existe pas
    }
    
    // Utiliser getComputedStyle pour obtenir la couleur réelle
    const currentColor = btn.style.color;

    // Vérifier si la couleur actuelle est celle du "like"  
    const isLiked = currentColor === "rgb(187, 82, 2)"; // #bb5202 en RGB

    // Changer la couleur
    btn.style.color = isLiked ? "black" : "#bb5202";  // Inverser la couleur

    // Envoi des données au serveur
    fetch('/recette/like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id_utilisateur: id_utilisateur,
            id_recette: id_recette,
            like: !isLiked
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur lors de l\'enregistrement du like.');
        }
        return response.json();
    })
    .then(data => {
        console.log('Réponse du serveur :', data);
    })
    .catch(error => {
        console.error('Erreur :', error);
        btn.style.color = isLiked ? "#bb5202" : "black"; // Rétablir la couleur en cas d'erreur
    });
  }



function togglePopup(){
  let popup = document.querySelector("#popup-overlay")
  popup.classList.toggle("open");
  setTimeout(() => {
    popup.style.display = "none";
  }, 3000);
}