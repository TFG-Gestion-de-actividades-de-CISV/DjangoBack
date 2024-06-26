from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

class CookieTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('token')

        if not token:
            return None

        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (token.user, token)
