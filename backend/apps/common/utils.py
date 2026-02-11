def get_user_condominium(user):
    if not user or not user.is_authenticated:
        return None
    return getattr(user, "condominium", None)
