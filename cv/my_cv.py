from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from cv.db import get_db

bp = Blueprint('my_cv', __name__)

@bp.route('/')
def index():
    return render_template('my_cv/index.html')