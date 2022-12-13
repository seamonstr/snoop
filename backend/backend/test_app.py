# GIVEN a call to create an app with a test setup provided
# WHEN the app object is returned
# THEN its configuration should contain the test setup

from .app import create_app


def test_test_configuration():
    test_env = {
        "env": "empty",  # Load the empty configuration
        "test_val": 20,  # Add a value
    }

    app = create_app(**test_env)
    # All above values should be set
    for k in test_env:
        assert app.config[k] == test_env[k], f"Unequal values for {k}"

    # Note no services are configured in the "empty" environment -
    # this should have no blueprints or extensions configured on it.
    assert len(app.blueprints) == 0
    assert len(app.extensions) == 0
