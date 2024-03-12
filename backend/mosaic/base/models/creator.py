""" Creator user django model definition """

from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from ..models.constants import _DOCUMENT_TYPE_CHOICES
from ..models.constants import _GENDER_CHOICES
from ..models.constants import _STATUS_CHOICES
from ..models.constants import PENDING

FILE_PATHS = {
    "profile_image": "creator/profile_image/creator_{}_profile_image_{}.{}",
}

FILE_EXTENSIONS = {
    "profile_image": (".jpeg", ".png", ".jpg")
}


class Creator(AbstractBaseUser):
    """ Extends native django user model adding new
    features to user definition.

    Python class representation for User database model

    """
    first_name = models.CharField("Nombre(s)", max_length=255)
    last_name = models.CharField("Apellido(s)", max_length=255)
    birth_date = models.DateField("Fecha de Nacimiento", 
        null=True, blank=True)
    email = models.EmailField("Correo", unique=True)
    document_type = models.CharField("Tipo de documento", max_length=255,
        choices=_DOCUMENT_TYPE_CHOICES, default="C.C.")
    document = models.CharField("Identificación", max_length=255, unique=True)
    address = models.CharField("Dirección", max_length=255)
    cellphone = models.CharField("Celular", max_length=255)
    gender = models.CharField("Género", max_length=255, 
        choices=_GENDER_CHOICES, default="Otro")
    status = models.CharField("Estado", max_length=255, choices=_STATUS_CHOICES,
        default=PENDING)
    token = models.IntegerField("Token cambio de contraseña",
        null=True, blank=True)
    profile_image = models.FileField("Imagen de perfil", 
        upload_to="user/profile_image", null=True, blank=True)

    USERNAME_FIELD = "document"

    class Meta:
        """ Sets human readable name """
        db_table = "base_creator"
        verbose_name = "Creador"
        verbose_name_plural = "Creadores"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"  

    def __str__(self):
        return (
            f"{self.pk}. {self.get_full_name()}"
            f" - {self.status}"
        )

    def upload_file(self, file_path, file):
        """ Saves files in model and s3 with custom name

        Parameters
        ----------

        file_path: str
            Contains the file path

        file: file
            Contain the file to save in the model

        Return
        ------

        result: boolean
            True if the file is save succesfull or False if  it is no saved succesfull
        """
        # pylint:disable=no-member
        if file_path not in FILE_PATHS:
            return False
        if not isinstance(file, InMemoryUploadedFile):
            if isinstance(file, File):
                file.name = ".pdf"
            else:
                return False
        if not file.name.endswith(FILE_EXTENSIONS[file_path]):
            return False
        timestamp = str(timezone.now().timestamp()).replace('.', '_')
        extension = file.name.split('.')[-1:][0]
        file.name = FILE_PATHS[file_path].format(
            self.pk,
            timestamp,
            extension
        )
        setattr(self, file_path, file)
        self.save()
        return True