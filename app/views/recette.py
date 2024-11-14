from flask import (Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for)
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
        nom_categorie = request.form['nom_categorie']
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
        if id_utilisateur and titres and description and nombre_personne and temps_preparation and temps_cuisson and etapes and difficulte:
            try:
                # Insérer la recette dans la base de données
                cursor = db.execute("SELECT id_categorie FROM categories WHERE nom_categorie = ?", (nom_categorie,)) 
                result = cursor.fetchone()
                if result: 
                    id_categorie = result[0]

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
                else: 
                    flash('Catégorie non trouvée.') 
                    return render_template('recette/creation_recette.html')

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

@recette_bp.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('q', '')  # Récupère la requête de recherche de l'utilisateur
    if query:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_ingredient, nom FROM ingredients WHERE nom LIKE ?", ('%' + query + '%',))
        results = cursor.fetchall()
        db.close()

        # Convertir les résultats en une liste de dictionnaires
        suggestions = [{'id': row['id_ingredient'], 'nom': row['nom']} for row in results]
        return jsonify(suggestions)
    return jsonify([])  # Retourne une liste vide si aucun résultat

@recette_bp.route('/aperitifs', methods=['GET', 'POST'])
def show_aperitifs():
    db = get_db()
    id_categorie = 1

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('SELECT r.titres, p.chemin_vers_le_fichier FROM recettes r JOIN photo_recette p ON r.id_recette = p.id_recette WHERE id_categorie = ?', (id_categorie,))

    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom de fichier
        recettes_traitees.append({'titres': recette['titres'], 'chemin_vers_le_fichier': nom_fichier})


    return render_template('recette/aperitifs.html', recettes=recettes_traitees)

@recette_bp.route('/entrees', methods=['GET', 'POST'])
def show_entrees():
    db = get_db()
    id_categorie = 2

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('SELECT r.titres, p.chemin_vers_le_fichier FROM recettes r JOIN photo_recette p ON r.id_recette = p.id_recette WHERE id_categorie = ?', (id_categorie,))

    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom de fichier
        recettes_traitees.append({'titres': recette['titres'], 'chemin_vers_le_fichier': nom_fichier})


    return render_template('recette/entrees.html', recettes=recettes_traitees)

@recette_bp.route('/plats', methods=['GET', 'POST'])
def show_plats():
    db = get_db()
    id_categorie = 3

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('SELECT r.titres, p.chemin_vers_le_fichier FROM recettes r JOIN photo_recette p ON r.id_recette = p.id_recette WHERE id_categorie = ?', (id_categorie,))

    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom de fichier
        recettes_traitees.append({'titres': recette['titres'], 'chemin_vers_le_fichier': nom_fichier})


    return render_template('recette/plats.html', recettes=recettes_traitees)

@recette_bp.route('/desserts', methods=['GET', 'POST'])
def show_desserts():
    db = get_db()
    id_categorie = 4

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('SELECT r.titres, p.chemin_vers_le_fichier FROM recettes r JOIN photo_recette p ON r.id_recette = p.id_recette WHERE id_categorie = ?', (id_categorie,))

    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom de fichier
        recettes_traitees.append({'titres': recette['titres'], 'chemin_vers_le_fichier': nom_fichier})


    return render_template('recette/desserts.html', recettes=recettes_traitees)

@recette_bp.route('/smoothies', methods=['GET', 'POST'])
def show_smoothies():
    db = get_db()
    id_categorie = 5

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('SELECT r.titres, p.chemin_vers_le_fichier FROM recettes r JOIN photo_recette p ON r.id_recette = p.id_recette WHERE id_categorie = ?', (id_categorie,))

    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom de fichier
        recettes_traitees.append({'titres': recette['titres'], 'chemin_vers_le_fichier': nom_fichier})


    return render_template('recette/smoothies.html', recettes=recettes_traitees)

@recette_bp.route('/boissons', methods=['GET', 'POST'])
def show_boissons():
    db = get_db()
    id_categorie = 6

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('SELECT r.titres, p.chemin_vers_le_fichier FROM recettes r JOIN photo_recette p ON r.id_recette = p.id_recette WHERE id_categorie = ?', (id_categorie,))

    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir uniquement le nom de fichier
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom de fichier
        recettes_traitees.append({'titres': recette['titres'], 'chemin_vers_le_fichier': nom_fichier})


    return render_template('recette/boissons.html', recettes=recettes_traitees)

