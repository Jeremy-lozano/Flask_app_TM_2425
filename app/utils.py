import functools
from flask import (Blueprint, app, flash, g, redirect, render_template, request, session, url_for)
import os
from werkzeug.utils import secure_filename
import uuid
from flask import current_app



# Ce décorateur est utilisé dans l'application Flask pour protéger certaines vues (routes)
# afin de s'assurer qu'un utilisateur est connecté avant d'accéder à une route 

def login_required(view):
    
    @functools.wraps(view)
    def wrapped_view(**kwargs):
    
        # Si l'utilisateur n'est pas connecté, il ne peut pas accéder à la route, il faut le rediriger vers la route auth.login
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view



def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

UPLOAD_FOLDER = os.path.join('app', 'static', 'imgs', 'photo_recette')

def upload_and_get_path(file):
    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Retourner un chemin relatif à 'static', comme Flask s'y attend
    return os.path.join('imgs', 'photo_recette', filename)





