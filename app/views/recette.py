from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db, close_db
from app.utils import *
import os
from app.utils import upload_and_get_path

# Routes /user/...
recette_bp = Blueprint('recette', __name__, url_prefix='/recette')

@recette_bp.route('/mes-recettes', methods=('GET', 'POST'))
@login_required
def show_recettes():
    user_id = session.get('user_id')
    db = get_db()

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('SELECT r.titres, p.chemin_vers_le_fichier FROM recettes r JOIN photo_recette p ON r.id_recette = p.id_recette WHERE id_utilisateur = ?', (user_id,))

    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom de fichier
        recettes_traitees.append({'titres': recette['titres'], 'chemin_vers_le_fichier': nom_fichier})


    return render_template('recette/mes_recettes.html', link=url_for('user.show_profile'), recettes=recettes_traitees)



@recette_bp.route('/creation', methods=['GET', 'POST'])
@login_required
def creation():
    if request.method == 'POST':

        titres = request.form['titres']
        id_categorie = request.form['id_categorie']
        description = request.form['description']
        nombre_personne = request.form['nombre_personne']
        temps_preparation = request.form['temps_preparation']
        temps_cuisson = request.form['temps_cuisson']
        etapes = request.form['etapes']
        difficulte = request.form['difficulte']
        id_utilisateur = session.get('user_id')

        # Récupérer le fichier téléchargé
        file = request.files.get('file')

        # On récupère la base de données
        db = get_db()

        # Vérifier que tous les champs nécessaires sont remplis
        if id_utilisateur and titres and id_categorie and description and nombre_personne and temps_preparation and temps_cuisson and etapes and difficulte:
            try:
                # Insérer la recette dans la base de données
                db.execute("INSERT INTO recettes (id_utilisateur, titres, id_categorie, description, nombre_personne, temps_preparation, temps_cuisson, etapes, difficulte) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           (id_utilisateur, titres, id_categorie, description, nombre_personne, temps_preparation, temps_cuisson, etapes, difficulte))
                
                # Récupérer l'ID de la recette nouvellement insérée
                id_recette = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                print(f"ID de la recette insérée : {id_recette}")

                # Si un fichier a été téléchargé, gérer l'upload et insérer l'image
                if file and file.filename != '':
                    chemin_vers_le_fichier = upload_and_get_path(file)  # Appel à la fonction d'upload
                    print(f"Chemin vers l'image : {chemin_vers_le_fichier}")
                    
                    # Insérer l'image associée à la recette dans la table photo_recette
                    db.execute("INSERT INTO photo_recette (id_recette, chemin_vers_le_fichier) VALUES (?, ?)", 
                               (id_recette, chemin_vers_le_fichier))
                
                # Valider les changements dans la base de données
                db.commit()

                flash('Recette créée avec succès !')
                print(f"Recette : {titres} ajoutée avec succès")

                return redirect(url_for('recette.validation'))

            except Exception as e:
                db.rollback()  # Annuler la transaction en cas d'erreur
                return redirect(url_for('recette.creation'))
        else:
            flash('Tous les champs sont obligatoires.')
            return render_template('recette/creation_recette.html')

    return render_template('recette/creation_recette.html')


@recette_bp.route('/validation', methods=['GET', 'POST'])
@login_required
def validation():

    return render_template('recette/validation.html')
     

