from threading import local

_store = local()


def set_current_user(user):
    _store.user = user


def get_current_user():
    return getattr(_store, "user", None)
