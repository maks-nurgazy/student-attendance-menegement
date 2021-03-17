from rest_framework_simplejwt.tokens import RefreshToken


def get_jwt_tokens_for_user(user, **kwargs):
    """
    Generates a refresh token for the valid user
    """
    refresh = RefreshToken.for_user(user)

    return str(refresh), str(refresh.access_token)
