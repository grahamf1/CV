from flask import (
    Blueprint, flash, render_template, request
)
from .db import add_comment

bp = Blueprint('my_cv', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']
        error = None

        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Password is required.'
        elif not comment:
            error = 'Comment is required.'

        if error is None:
            try:
                add_comment(name, email, comment)
                flash('Comment added successfully.')
            except Exception as e:
                error = f"There was an issue submitting your comment: {str(e)}"

        if error:
            flash(error)
                
    return render_template('index.html')