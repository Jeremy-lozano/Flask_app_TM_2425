from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

# Routes /...
home_bp = Blueprint('home', __name__)



# Route /
@home_bp.route('/', methods=('GET', 'POST'))
def landing_page():
    if 'user_logged_in' in session:
        return render_template('home/index.html', link=url_for('user.show_profile'))
    else:
        return render_template('home/index.html', link=url_for('user.button_connection'))

# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route('/<path:text>', methods=['GET', 'POST'])
def not_found_error(text):
    return render_template('home/404.html'), 404
