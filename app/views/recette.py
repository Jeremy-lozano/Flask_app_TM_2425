import sqlite3
from flask import (Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for)
from app.db import db
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
    cursor = db.execute('SELECT r.titres, p.chemin_vers_le_fichier '
                        'FROM recettes r '
                        'JOIN photo_recette p ON r.id_recette = p.id_recette '
                        'WHERE id_utilisateur = ?', (user_id,))

    recettes = cursor.fetchall()
    db.close()

    # Traiter les résultats pour obtenir le chemin relatif pour les fichiers statiques
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom du fichier

        # Convertir le chemin en utilisant des barres obliques normales (i.e. '/')
        chemin_relatif = os.path.normpath(os.path.join('imgs', 'photo_recette', nom_fichier)).replace(os.sep, '/')

        # Ajouter à la liste des recettes traitées
        recettes_traitees.append({
            'titres': recette['titres'],
            'chemin_vers_le_fichier': chemin_relatif
        })

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

        id_ingredients = request.form.getlist('id_ingredient[]')  # Liste des ID des ingrédients
        quantites = request.form.getlist('quantite[]')  # Liste des quantités

        # On récupère la base de données
        db = get_db()

        print("Données du formulaire :", {
            "id_utilisateur": id_utilisateur,
            "titres": titres,
            "nom_categorie": nom_categorie,
            "description": description,
            "nombre_personne": nombre_personne,
            "temps_preparation": temps_preparation,
            "temps_cuisson": temps_cuisson,
            "etapes": etapes,
            "difficulte": difficulte,
            "id_ingredients": id_ingredients,
            "quantites": quantites,
            "file": file
        })  # Log des données reçues

        # Vérifier que tous les champs nécessaires sont remplis
        if id_utilisateur and titres and description and nombre_personne and temps_preparation and temps_cuisson and etapes and difficulte:
            try:
                # Insérer la recette dans la base de données
                cursor = db.execute("SELECT id_categorie FROM categories WHERE nom_categorie = ?", (nom_categorie,))
                result = cursor.fetchone()
                print("Résultat de la requête de catégorie :", result)  # Log du résultat de la requête

                if result:
                    id_categorie = result[0]

                    db.execute("INSERT INTO recettes (id_utilisateur, titres, id_categorie, description, nombre_personne, temps_preparation, temps_cuisson, etapes, difficulte) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (id_utilisateur, titres, id_categorie, description, nombre_personne, temps_preparation, temps_cuisson, etapes, difficulte))

                    # Récupérer l'ID de la recette nouvellement insérée
                    id_recette = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                    print(f"ID de la recette insérée : {id_recette}")

                    for id_ingredient, quantite in zip(id_ingredients, quantites):
                        if id_ingredient and quantite:
                            db.execute("INSERT INTO utilise (id_recette, id_ingredient, quantite) VALUES (?, ?, ?)",
                                       (id_recette, id_ingredient, quantite))
                            print(f"Ingrédient {id_ingredient} avec quantité {quantite} ajouté à la recette {id_recette}")

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
                print(f"Erreur lors de la création de la recette : {e}")  # Log de l'exception
                flash(f"Erreur lors de la création de la recette : {str(e)}")
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
    query = request.args.get('q', '').strip()  # Récupère la requête et supprime les espaces inutiles
    if query:
        db = get_db()
        cursor = db.cursor()
        # Modifier la requête pour rechercher uniquement les noms qui commencent par les lettres saisies
        cursor.execute("SELECT id_ingredient, nom FROM ingredients WHERE nom LIKE ?", (query + '%',))
        results = cursor.fetchall()
        db.close()
        # Convertir les résultats en une liste de dictionnaires
        suggestions = [{'id_ingredient': row['id_ingredient'], 'nom': row['nom']} for row in results]
        return jsonify(suggestions)
    return jsonify([])  # Retourne une liste vide si aucune requête n'est fournie


@recette_bp.route('/aperitifs', methods=['GET', 'POST'])
def show_aperitifs():
    db = get_db()
    user_id = session.get('user_id')

    id_categorie = 1  # ID de la catégorie "Apéritifs"

    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('''
        SELECT r.titres, p.chemin_vers_le_fichier, r.id_recette
        FROM recettes r
        JOIN photo_recette p ON r.id_recette = p.id_recette
        WHERE r.id_categorie = ?
    ''', (id_categorie,))

    recettes = cursor.fetchall()

    # Traiter les résultats pour obtenir le chemin relatif pour les fichiers statiques
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
    db.close() 

    # Rendre la page avec les recettes traitées
    return render_template('recette/aperitifs.html', recettes=recettes_traitees, categorie="aperitifs")

@recette_bp.route('/entrees', methods=['GET', 'POST'])
def show_entrees():
    db = get_db()
    
    id_categorie = 2
    user_id = session.get('user_id')

    # Requête pour récupérer les titres des recettes et les chemins des photos
    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('''
        SELECT r.titres, p.chemin_vers_le_fichier, r.id_recette
        FROM recettes r
        JOIN photo_recette p ON r.id_recette = p.id_recette
        WHERE r.id_categorie = ?
    ''', (id_categorie,))

    recettes = cursor.fetchall()

    # Traiter les résultats pour obtenir le chemin relatif pour les fichiers statiques
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
    db.close()
    # Rendre la page avec les recettes traitées
    return render_template('recette/entrees.html', recettes=recettes_traitees,categorie="entrees")

@recette_bp.route('/plats', methods=['GET', 'POST'])
def show_plats():
    db = get_db()
    
    id_categorie = 3
    user_id = session.get('user_id')

    # Requête pour récupérer les titres des recettes et les chemins des photos
    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('''
        SELECT r.titres, p.chemin_vers_le_fichier, r.id_recette
        FROM recettes r
        JOIN photo_recette p ON r.id_recette = p.id_recette
        WHERE r.id_categorie = ?
    ''', (id_categorie,))

    recettes = cursor.fetchall()

    # Traiter les résultats pour obtenir le chemin relatif pour les fichiers statiques
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
    db.close()

    # Rendre la page avec les recettes traitées
    return render_template('recette/plats.html', recettes=recettes_traitees,categorie="plats")

@recette_bp.route('/desserts', methods=['GET', 'POST'])
def show_desserts():
    db = get_db()
    
    id_categorie = 4
    user_id = session.get('user_id')

    # Requête pour récupérer les titres des recettes et les chemins des photos
    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('''
        SELECT r.titres, p.chemin_vers_le_fichier, r.id_recette
        FROM recettes r
        JOIN photo_recette p ON r.id_recette = p.id_recette
        WHERE r.id_categorie = ?
    ''', (id_categorie,))

    recettes = cursor.fetchall()

    # Traiter les résultats pour obtenir le chemin relatif pour les fichiers statiques
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
    db.close()

    # Rendre la page avec les recettes traitées
    return render_template('recette/desserts.html', recettes=recettes_traitees, categorie="desserts")

@recette_bp.route('/smoothies', methods=['GET', 'POST'])
def show_smoothies():
    db = get_db()
    
    id_categorie = 5
    user_id = session.get('user_id')

    # Requête pour récupérer les titres des recettes et les chemins des photos
    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('''
        SELECT r.titres, p.chemin_vers_le_fichier, r.id_recette
        FROM recettes r
        JOIN photo_recette p ON r.id_recette = p.id_recette
        WHERE r.id_categorie = ?
    ''', (id_categorie,))

    recettes = cursor.fetchall()

    # Traiter les résultats pour obtenir le chemin relatif pour les fichiers statiques
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
    db.close()
    # Rendre la page avec les recettes traitées
    return render_template('recette/smoothies.html', recettes=recettes_traitees,categorie="smoothies")

@recette_bp.route('/boissons', methods=['GET', 'POST'])
def show_boissons():
    db = get_db()
    
    id_categorie = 6
    user_id = session.get('user_id')

    # Requête pour récupérer les titres des recettes et les chemins des photos
    # Requête pour récupérer les titres des recettes et les chemins des photos
    cursor = db.execute('''
        SELECT r.titres, p.chemin_vers_le_fichier, r.id_recette
        FROM recettes r
        JOIN photo_recette p ON r.id_recette = p.id_recette
        WHERE r.id_categorie = ?
    ''', (id_categorie,))

    recettes = cursor.fetchall()

    # Traiter les résultats pour obtenir le chemin relatif pour les fichiers statiques
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
    db.close()
    # Rendre la page avec les recettes traitées
    return render_template('recette/boissons.html', recettes=recettes_traitees)


@recette_bp.route('/<titres>', methods=['GET', 'POST'])
def detail_recette(titres):
    db = get_db()

    user_id = session.get('user_id')

    # Requête pour récupérer toutes les informations de la recette, les photos, les ingrédients et le username de l'utilisateur
    cursor = db.execute('''
        SELECT r.id_recette, r.titres, r.description, r.nombre_personne, r.temps_preparation,
               r.temps_cuisson, r.etapes, r.difficulte, p.chemin_vers_le_fichier,
               ri.id_ingredient, ri.quantite, i.nom AS ingredient_nom,
               u.username, u.prenom
        FROM recettes r
        LEFT JOIN photo_recette p ON r.id_recette = p.id_recette
        LEFT JOIN utilise ri ON r.id_recette = ri.id_recette
        LEFT JOIN ingredients i ON ri.id_ingredient = i.id_ingredient
        LEFT JOIN utilisateurs u ON r.id_utilisateur = u.id_utilisateur
        WHERE r.titres = ?
    ''', (titres,))

    # Traiter les résultats
    recette = cursor.fetchall()

    # Vérifier si des résultats ont été trouvés
    if recette:
        # Initialisation des variables pour la recette et les ingrédients
        recette_data = {
            'id_recette': recette[0]['id_recette'],
            'titres': recette[0]['titres'],
            'description': recette[0]['description'],
            'nombre_personne': recette[0]['nombre_personne'],
            'temps_preparation': recette[0]['temps_preparation'],
            'temps_cuisson': recette[0]['temps_cuisson'],
            'etapes': recette[0]['etapes'],
            'difficulte': recette[0]['difficulte'],
            'chemin_vers_le_fichier': None,
            'username': recette[0]['username'],   # Ajouter le username de l'utilisateur
            'ingredients': [],            
        }

        # Extraire le chemin relatif de l'image si elle existe
        if recette[0]['chemin_vers_le_fichier']:
            # Extraction du nom du fichier
            nom_fichier = os.path.basename(recette[0]['chemin_vers_le_fichier'])
            # Créer le chemin relatif à 'static'
            recette_data['chemin_vers_le_fichier'] = os.path.join('imgs', 'photo_recette', nom_fichier).replace(os.sep, '/')

        # Extraire tous les ingrédients associés à la recette
        for row in recette:
            if row['ingredient_nom']:
                recette_data['ingredients'].append({
                    'ingredient_nom': row['ingredient_nom'],
                    'quantite': row['quantite']
                })

        # Passer les données de la recette et des ingrédients au template
        return render_template('recette/recette_detail.html', recette=recette_data)

    else:
        # Si aucune recette n'est trouvée
        flash('Recette non trouvée.')
        return redirect(url_for('home.index'))
    

@recette_bp.route("/resultat/<recherche>")
def resultat(recherche):
    db = get_db()
    user_id = session.get('user_id')

    
    # Requête SQL pour récupérer les recettes contenant le terme recherché dans le titre
    cursor = db.execute('''
        SELECT r.id_recette, r.titres, p.chemin_vers_le_fichier
        FROM recettes r
        LEFT JOIN photo_recette p ON r.id_recette = p.id_recette
        WHERE r.titres LIKE ?
    ''', (f'%{recherche}%',))  # Utilisation de LIKE pour rechercher dans le titre
    recettes = cursor.fetchall()
    
    
    # Traiter les chemins pour qu'ils soient relatifs
    recettes_traitees = []
    for recette in recettes:
        chemin_complet = recette['chemin_vers_le_fichier']
        if chemin_complet:  # Vérifier si le chemin est défini
            nom_fichier = os.path.basename(chemin_complet)  # Extraire le nom du fichier
            # Convertir le chemin complet en un chemin relatif à partir de 'static/'
            chemin_relatif = os.path.join('imgs', 'photo_recette', nom_fichier)
            # Remplacer les barres obliques inverses par des barres obliques normales
            chemin_relatif = chemin_relatif.replace("\\", "/")
        else:
            chemin_relatif = None  # Pas de chemin d'image disponible
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
            'is_liked': is_liked,
        })
    
    # Affiche la recherche de l'utilisateur en tant que titre
    return render_template(
        "recette/resultats_recherche.html",
        recherche=recherche,
        recettes=recettes_traitees
    )

@recette_bp.route('/mes-favoris', methods=('GET', 'POST'))
@login_required
def show_favoris():
    user_id = session.get('user_id')
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
    db.close()

    return render_template('user/favoris.html', recettes=recettes_traitees)


@recette_bp.route('/like', methods=('GET', 'POST'))
@login_required
def like():
    data = request.get_json()
    id_utilisateur = data.get('id_utilisateur')
    id_recette = data.get('id_recette')
    like_action = data.get('like')  # True pour like, False pour unlike

    if not id_utilisateur or not id_recette:
        return jsonify({'error': 'Données invalides'}), 400

    db = get_db()

    try:
        if like_action:
            # Vérifier si le like existe déjà
            cursor = db.execute(
                "SELECT 1 FROM aimer WHERE id_utilisateur = ? AND id_recette = ?",
                (id_utilisateur, id_recette)
            )
            if cursor.fetchone():
                return jsonify({'message': 'Le like existe déjà'}), 200

            # Ajouter le like
            db.execute(
                "INSERT INTO aimer (id_utilisateur, id_recette) VALUES (?, ?)",
                (id_utilisateur, id_recette)
            )
            db.commit()
            return jsonify({'message': 'Like ajouté avec succès'}), 201
        else:
            # Supprimer le like
            db.execute(
                "DELETE FROM aimer WHERE id_utilisateur = ? AND id_recette = ?",
                (id_utilisateur, id_recette)
            )
            db.commit()
            return jsonify({'message': 'Like supprimé avec succès'}), 200

    except sqlite3.Error as e:
        print("Erreur SQLite :", e)
        return jsonify({'error': 'Erreur serveur'}), 500