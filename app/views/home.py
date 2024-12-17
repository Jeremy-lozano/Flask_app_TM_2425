from pydoc import apropos
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
import os
from app.db.db import get_db, close_db
# Routes /...
home_bp = Blueprint('home', __name__)


# Route /
@home_bp.route('/', methods=['GET', 'POST'])
def landing_page():
    user_id = session.get('user_id')
        
    if request.method == "POST":
        # On récupère la recherche de l'utilisateur
        recherche = request.form["search"]
        # Redirection vers la page de résultats avec la recherche comme paramètre
        return redirect(url_for("recette.resultat", recherche=recherche))
    db = get_db()

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('''
        SELECT r.id_recette, r.titres, p.chemin_vers_le_fichier
        FROM recettes r
        LEFT JOIN photo_recette p ON r.id_recette = p.id_recette
    ''')  # Utilisation de LIKE pour rechercher dans le titre
    recettes = cursor.fetchall()
    
    
    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom du fichier

        # Convertir le chemin complet en un chemin relatif à partir de 'static/'
        chemin_relatif = os.path.join('imgs', 'photo_recette', nom_fichier)

        # Remplacer les barres obliques inverses par des barres obliques normales
        chemin_relatif = chemin_relatif.replace("\\", "/")
        if user_id:
            cursor_like = db.execute('''
                SELECT 1 FROM aimer WHERE id_utilisateur = ? AND id_recette = ?
            ''', (user_id, recette['id_recette']))
            is_liked = cursor_like.fetchone() is not None  # Vérifier si une ligne existe dans la table "aimer"
        else:
            is_liked = False

      

        # Ajouter à la liste des recettes traitées
        recettes_traitees.append({
            'id_utilisateur': user_id,
            'id_recette': recette['id_recette'],
            'titres': recette['titres'],
            'chemin_vers_le_fichier': chemin_relatif,
            'is_liked': is_liked
        })
    print("User ID:", user_id)

    db.close()
    return render_template('home/index.html', link=url_for('user.show_profile'), recettes=recettes_traitees)


# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route('/<path:text>', methods=['GET', 'POST'])
def not_found_error(text):
    return render_template('home/404.html'), 404


@home_bp.route('/a-propos', methods=['GET', 'POST'])
def apropos():
    return render_template('home/a-propos.html')






