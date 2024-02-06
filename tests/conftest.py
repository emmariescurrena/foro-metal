"""Fixtures for tests"""

import pytest
from src import create_app, db


@pytest.fixture()
def test_app():
    """Creates app for testing"""

    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            yield test_client
