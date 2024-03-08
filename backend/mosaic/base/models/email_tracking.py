"""Contains the email_tracking model"""
from django.db import models
from django_extensions.db.models import TimeStampedModel

SENT = "sent"
READ = "read"
ERROR = "error"

_STATUSES_CHOICES = (
    (SENT, "Enviado"),
    (READ, "Leído"),
    (ERROR, "Error al enviar")
)

CLIENT = "cliente"
ADMIN = "administrador"

_MODULES_CHOICES = (
    (CLIENT, "Clientes"),
    (ADMIN, "Administradores")
)


class EmailTracking(TimeStampedModel):
    """
    Python class representation for EmailTracking database model
    """
    id_module = models.IntegerField("ID del módulo")
    type_module = models.CharField(
        "Tipo del módulo", max_length=255, choices=_MODULES_CHOICES,
        default=CLIENT)
    subject = models.CharField("Asunto", max_length=255, null=True, blank=True)
    receivers = models.CharField("Destinatarios", max_length=255)
    content = models.TextField("Contenido", null=True, blank=True)
    status = models.CharField(
        "Estado del correo", max_length=255, choices=_STATUSES_CHOICES,
        default=SENT)
    confirmation_token = models.CharField(
        "Token de confirmación", max_length=255)

    class Meta:
        """Sets human readable name"""

        db_table = "base_email_tracking"
        verbose_name = "Seguimiento de correo electrónico"
        verbose_name_plural = "Seguimientos de correos electrónicos"

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.subject} - {self.status}"
