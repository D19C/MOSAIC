""" Contains User endpoint definition """

from jwt import InvalidTokenError, encode, decode

from cerberus import Validator

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import timedelta
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..helpers.envs import getenv

from ..models.auth import Auth
from ..models.constants import ADMIN, USER, CREATOR
from ..models.creator import Creator
from ..models.user import User


def _get_user_type(obj):
    """ Retrieves user type accorging to object granted.

    Parameter
    ---------

    obj: Model object (User or Root)

    Return
    ------

    str: User type

    """
    if isinstance(obj, Creator):
        return CREATOR
    elif isinstance(obj, User):
        return ADMIN if obj.rol == ADMIN else USER
    else:
        return USER


class AuthApi(APIView):
    """ Defines the HTTP verbs to auth model management. """

    def post(self, request):
        """ Creates a new session.

        Parameters
        ----------

        request: dict
            Contains http transaction information.

        Returns
        -------

        Response: (dict, int)
            Body response and status code.

        """
        # pylint: disable=no-self-use,no-member
        validator = Validator({
            "user": {"required": True, "type": "string"},
            "password": {"required": True, "type": "string", "minlength": 7},
            "keep_logged_in": {"required": True, "type": "boolean"},
            "type": {
                "required": True, "type": "string",
                "allowed": [CREATOR, ADMIN, USER]
            }
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "Cuerpo con estructura inválida",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        if request.data["type"] in [ADMIN, USER]:
            obj = User.objects.filter(
                Q(email=request.data["user"]) |
                Q(document=request.data["user"]),
                rol=request.data["type"]
            ).first()

        elif request.data["type"] == CREATOR:
            obj = Creator.objects.filter(
                Q(username=request.data["user"])
            ).first()

        if not obj:
            return Response({
                "code": "user_not_found",
                "detailed": f"{_get_user_type(obj)} no encontrado o inactivo"
            }, status=status.HTTP_404_NOT_FOUND)

        if not check_password(request.data["password"], obj.password):
            return Response({
                "code": "incorrect_password",
                "detailed": "Contraseña incorrecta"
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = get_random_string(30)

        token = encode({
            "expiration_date": str(timezone.now() + (
                timedelta(hours=getenv("TOKEN_EXP_HOURS"))
                if not request.data["keep_logged_in"]
                else timedelta(days=getenv("KEEP_LOGGED_IN_TOKEN_EXP_DAYS"))
            )),
            "email": obj.email if isinstance(obj, User) else None,
            "username": obj.username if isinstance(obj, Creator) else None,
            "type": _get_user_type(obj),
            "refresh": refresh
        }, settings.SECRET_KEY, algorithm="HS256").decode("utf-8")

        Auth.objects.create(token=token)

        if isinstance(obj, User):
            User.objects.filter(email=obj.email).update(
                last_login=timezone.now())

            return Response({
                "id": obj.pk,
                "token": token,
                "refresh": refresh,
                "email": obj.email,
                "cellphone": obj.cellphone,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "gender": obj.gender,
                "rol": obj.rol,
                "status": obj.status,
                "document": obj.document,
                "document_type": obj.document_type,
                "type": _get_user_type(obj)
            }, status=status.HTTP_201_CREATED)
            
        if isinstance(obj, Creator):
            Creator.objects.filter(username=obj.username).update(
                last_login=timezone.now())

            return Response({
                "id": obj.pk,
                "token": token,
                "refresh": refresh,
                "username": obj.username,
                "type": _get_user_type(obj)
            }, status=status.HTTP_201_CREATED)

        return Response({
            "code": "unauthorized",
            "detailed": "Sesión expirada o no autorizado"
        }, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):  # pylint: disable=no-self-use
        """ Disables a session.

        Parameters
        ----------

        request: dict
            Contains http transaction information.

        Returns
        -------

        Response: int
            Response status code.

        """
        # pylint: disable=no-member
        header = request.headers.get("Authorization", None)

        if (not header or len(header.split(" ")) != 2 or
                header.split(" ")[0].lower() != "bearer"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        session = Auth.objects.filter(token=header.split(" ")[1])
        if not session:
            return Response(status=status.HTTP_404_NOT_FOUND)

        session.update(is_disabled=True)
        return Response(status=status.HTTP_200_OK)


class RefreshTokenApi(APIView):
    """ Defines the HTTP verbs to refresh token. """

    def patch(self, request, *args, **kwargs):
        # pylint: disable=no-self-use,unused-argument
        """ Refreshes a token.

        Parameters
        ----------

        request: dict
            Contains http transaction information.

        Returns
        -------

        Response: (dict, int)
            Body response and status code.

        """
        # pylint: disable=no-member
        header = request.headers.get("Authorization", None)

        if (not header or len(header.split(" ")) != 2 or
                header.split(" ")[0].lower() != "bearer"):
            return Response({
                "code": "invalid_header",
                "detailed": "Encabezado con estructura inválida"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = decode(header.split(" ")[1], settings.SECRET_KEY)
        except InvalidTokenError:
            return Response({
                "code": "invalid_token",
                "detailed": "Token inválido"
            }, status=status.HTTP_400_BAD_REQUEST)

        if token["refresh"] != kwargs["refresh"]:
            return Response({
                "code": "do_not_have_permission",
                "detailed": "No tienes permiso para ejecutar esta acción."
            }, status=status.HTTP_403_FORBIDDEN)

        type_token = token["type"]
        if type_token in [USER, ADMIN]:
            obj = User.objects.filter(
                email=token["email"], document=token["document"], rol=type_token).first()
        elif type_token == CREATOR:
            obj = Creator.objects.filter(
                username=token["username"]).first()
        if not obj:
            return Response({
                "code": "user_not_found",
                "detailed": f"{type_token} no encontrado o inactivo"
            }, status=status.HTTP_404_NOT_FOUND)

        refresh = get_random_string(30)
        token = encode({
            "expiration_date": str(
                (timezone.now() + timedelta(days=getenv("TOKEN_EXP_DAYS")))),
            "email": obj.email,
            "type": type_token,
            "refresh": refresh
        }, settings.SECRET_KEY, algorithm="HS256").decode("utf-8")

        session = Auth.objects.filter(token=header.split(" ")[1])
        if not session:
            return Response({
                "code": "token_not_found",
                "detailed": "Token no existe en la base de datos"
            }, status=status.HTTP_404_NOT_FOUND)

        session.update(token=token)

        if type_token in [USER, ADMIN]:
            User.objects.filter(email=obj.email).update(
                last_login=timezone.now())
            Auth.objects.create(token=token)
            return Response({
                "id": obj.pk,
                "token": token,
                "refresh": refresh,
                "email": obj.email,
                "cellphone": obj.cellphone,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "gender": obj.gender,
                "rol": obj.rol,
                "status": obj.status,
                "document": obj.document,
                "document_type": obj.document_type,
                "type": _get_user_type(obj)
            }, status=status.HTTP_201_CREATED)

        if isinstance(obj, Creator):
            Creator.objects.filter(username=obj.username).update(
                last_login=timezone.now())

            return Response({
                "id": obj.pk,
                "token": token,
                "refresh": refresh,
                "username": obj.username,
                "type": _get_user_type(obj)
            }, status=status.HTTP_201_CREATED)

        return Response({
            "code": "unauthorized",
            "detailed": "Sesión expirada o no autorizado"
        }, status=status.HTTP_401_UNAUTHORIZED)


class NewPasswordApi(APIView):
    """ Defines the HTTP verbs to new password. """

    def patch(self, request, user_pk):
        # pylint: disable=no-self-use,unused-argument,no-member
        """ Creates a new password for users.

        Parameters
        ----------

        request: dict
            Contains http transaction information.

        user_pk: int
            Contains the primary key of the user

        Returns
        -------

        Response: (dict, int)
            Body response and status code.

        """
        validator = Validator({
            "token": {"required": True, "type": "integer", "empty": False},
            "new_password": {"required": True, "type": "string", "minlength": 8}
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "Cuerpo con estructura inválida",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(
            pk=user_pk, token=request.data["token"]).first()

        if not user:
            return Response({
                "code": "user_not_found",
                "detailed": "Usuario no encontrado o datos inválidos"
            }, status=status.HTTP_404_NOT_FOUND)

        if user.password == request.data["new_password"]:
            return Response({
                "code": "password_already_setted",
                "detailed": "Contraseña ya asignada previamente"
            }, status=status.HTTP_409_CONFLICT)

        user.password = make_password(request.data["new_password"])
        user.save()

        return Response(status=status.HTTP_200_OK)
