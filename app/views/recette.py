from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db, close_db
from app.utils import *

# Routes /user/...
recette_bp = Blueprint('recette', __name__, url_prefix='/recette')

@recette_bp.route('/mes-recette', methods=('GET', 'POST'))
@login_required
def show_recettes():
        
        return render_template('recette/mes_recettes.html')

@recette_bp.route('/creation', methods=('GET', 'POST'))
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


        # On récupère la base de donnée
        db = get_db()

        # Si le nom d'utilisateur et le mot de passe ont bien une valeur
        # on essaie d'insérer l'utilisateur dans la base de données
        if titres and id_categorie and description and nombre_personne and temps_preparation and temps_cuisson and etapes and difficulte:
            try:
                db.execute("INSERT INTO recettes (titres, id_categorie, description, nombre_personne, temps_preparation, temps_cuisson, etapes, difficulte) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (titres, id_categorie, description, nombre_personne, temps_preparation, temps_cuisson, etapes, difficulte))   
                # db.commit() permet de valider une modification de la base de données
                db.commit()
                
                close_db()
                # On ferme la connexion à la base de données pour éviter les fuites de mémoire
                
            except db.IntegrityError:
                flash('une erreur sest produite')
                return redirect(url_for('recette.creation'))
            
            return render_template('home/index.html')
        else:
             flash('erreur')
             return render_template('recette/creation_recette.html')
               
    else:
        return render_template('recette/creation_recette.html')
