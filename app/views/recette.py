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
def creation():
        
        return render_template('recette/creation_recette.html')

