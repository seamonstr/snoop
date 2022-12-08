from . import models


def test_user():
    u = models.User(username="bob", pwd_hash="somehash")
    # Literal test; do the fields get set correctly via the constructor?
    assert u.username == "bob" and u.pwd_hash == "somehash"


def test_user_password_hashing():
    u = models.User(username="bob")
    u.set_hash_from_password("mypasswd")
    assert u.check_password_hash("mypasswd")
    assert not u.check_password_hash("some_rubbish_password")
    assert not u.check_password_hash("")
    assert not u.check_password_hash(None)
