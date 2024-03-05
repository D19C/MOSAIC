""" Contains the Auth model """
from django.db import models


class Auth(models.Model):
    """ Auth definition for sessions. """

    creation_date = models.DateTimeField(auto_now_add=True)
    is_disabled = models.BooleanField(default=False)
    token = models.TextField("Token", max_length=700)

    class Meta:  # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        db_table = "base_auth"
        verbose_name = "Sesión"
        verbose_name_plural = "Sesiones"

        indexes = [
            models.Index(
                fields=["token"], name="auth_token_idx"
            )
        ]

    def __str__(self):
        return str(self.token)
