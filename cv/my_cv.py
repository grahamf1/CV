from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from cv.db import get_db

bp = Blueprint('my_cv', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']
        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Password is required.'
        elif not comment:
            error = 'Comment is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO feedback (name, email, comment) VALUES (?, ?, ?)',
                    (name, email, comment)
                )
                db.commit()
                flash('Comment added successfully.')
            except:
                error = "There was an issue submitting your comment."
        
        flash(error)

    return render_template('index.html')