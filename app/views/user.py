from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
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
    # Affichage de la page principale de l'application
    return render_template('user/compte.html')