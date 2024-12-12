import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cv import create_app

def test_create_app():
    app = create_app()
    assert app is not None

def test_create_app_test_config():
    app = create_app(test_config={'TESTING': True})
    assert app.config['TESTING']

def test_blueprint_registered():
    app = create_app()
    assert 'my_cv' in app.blueprints

def test_root_url_rule():
    app = create_app()
    rules = [str(rule) for rule in app.url_map.iter_rules()]
    assert '/' in rules