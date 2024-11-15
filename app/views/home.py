from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
import os
from app.db.db import get_db, close_db
# Routes /...
home_bp = Blueprint('home', __name__)


# Route /
@home_bp.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == "POST":
        # On récupère la recherche de l'utilisateur
        recherche = request.form["search"]
        # Redirection vers la page de résultats avec la recherche comme paramètre
        return redirect(url_for("recette.resultat", recherche=recherche))
    db = get_db()

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('''
        SELECT r.titres, p.chemin_vers_le_fichier
        FROM recettes r
        JOIN photo_recette p ON r.id_recette = p.id_recette
    ''')
    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom du fichier

        # Convertir le chemin complet en un chemin relatif à partir de 'static/'
        chemin_relatif = os.path.join('imgs', 'photo_recette', nom_fichier)

        # Remplacer les barres obliques inverses par des barres obliques normales
        chemin_relatif = chemin_relatif.replace("\\", "/")

        # Ajouter à la liste des recettes traitées
        recettes_traitees.append({
            'titres': recette['titres'],
            'chemin_vers_le_fichier': chemin_relatif
        })


    return render_template('home/index.html', link=url_for('user.show_profile'), recettes=recettes_traitees)


# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route('/<path:text>', methods=['GET', 'POST'])
def not_found_error(text):
    return render_template('home/404.html'), 404
