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