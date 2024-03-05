""" This module contains all the tasks that are used in the project. """
from huey.contrib.djhuey import task

from ..models.auth import Auth


@task()
def delete_diseble_auth():
    """ Delete all disabled auths. """
    disabled_auths = Auth.objects.filter(is_disabled=True).all()
    for auth in disabled_auths:
        auth.delete()
