from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db, close_db
from app.utils import *

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/connexion', methods=('GET', 'POST'))
def button_connection():
        
        return render_template('user/bouton_connexion.html')

    
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required
def show_profile():
    user_id = session.get('user_id')

    # Si l'id de l'utilisateur dans le cookie session est nul, cela signifie que l'utilisateur n'est pas connecté
    # On met donc l'attribut 'user' de l'objet 'g' à None
    if user_id is None:
        g.recette = None

    # Si l'id de l'utilisateur dans le cookie session n'est pas nul, on récupère l'utilisateur correspondant et on stocke
    # l'utilisateur comme un attribut de l'objet 'g'
    else:
         # On récupère la base de données et on récupère l'utilisateur correspondant à l'id stocké dans le cookie session
        db = get_db()
        g.recette = db.execute('SELECT * FROM aimer WHERE id_utilisateur = ?', (user_id,)).fetchone()
        # On ferme la connexion à la base de données pour éviter les fuites de mémoire
        close_db()

    return render_template('user/compte.html')

