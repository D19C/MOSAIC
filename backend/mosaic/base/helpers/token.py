""" Handler for tokens """
import datetime as dt
from jwt import decode, InvalidTokenError

from django.conf import settings
from django.utils import timezone

from ..models.admin import Admin
from ..models.auth import Auth
from ..models.constants import CREATOR, USER
from ..models.creator import Creator
from ..models.user import User


class TokenHandler:
    """ Controls all the token functionalities for sessions """

    def get_payload(self, request):  # pylint: disable=no-self-use
        """ Returns token payload if is enabled or active.

        Parameter
        ---------

        request: dict
            Request information

        Return
        ------

        token, user: tuple 
            Token if it is active or enabled, else None

        """
        # pylint: disable=no-member
        header = request.headers.get("Authorization", None)
        if (not header or len(header.split(" ")) != 2 or
                header.split(" ")[0].lower() != "bearer"):
            return None, None

        try:
            token = decode(header.split(" ")[1], settings.SECRET_KEY)
        except InvalidTokenError:
            return None, None

        try:
            expiration_date = dt.datetime.strptime(
                token['expiration_date'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            expiration_date = dt.datetime.strptime(
                token['expiration_date'], '%Y-%m-%d %H:%M:%S.%f%z')

        db_token = Auth.objects.filter(token=header.split(" ")[1]).first()

        if (not db_token or db_token.is_disabled or
                expiration_date < timezone.now()):
            return None, None

        if token["type"] == USER:
            user = User.objects.filter(
                email=token["email"], rol=token["type"]).first()
        elif token["type"] == CREATOR:
            user = Creator.objects.filter(username=token["username"]).first()
        else:
            user = Admin.objects.filter(username=token["username"]).first()

        if not user:
            return None, None

        return token, user