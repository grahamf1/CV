import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is not None:
        app.config.from_pyfile(test_config)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import my_cv
    app.register_blueprint(my_cv.bp)
    app.add_url_rule('/', endpoint='index')

    return app

app = create_app()