""" Email helper """

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from huey.contrib.djhuey import task

# pylint:disable=relative-beyond-top-level, broad-except
from .envs import getenv

from ..models.email_template import EmailTemplate
from ..models.email_tracking import EmailTracking
from ..models.email_tracking import ERROR


_HEADER_MESSAGE = (
    '<div style="font-size:16px;background: #fff;border: 3px solid;'
    'min-width: 300px;max-width: 800px;padding-top: 40px !important;'
    'padding-bottom: 40px !important;border-radius: 13px; text-align:justify; '
    'padding:20px;">'
    '<div style="text-align:center">'
    '</div><br>'
)

_FOOTER_MESSAGE = (
    '<br><br>Atentamente:<br>Mosaic<br><br>'
)


@task()
def send_template_email(
    email_id,
    params,
    receivers,
    subject_params={},
    tracking_dict={}
):
    """ Sends an template email to given receivers.

    Parameters
    ----------

    email_id: str
        Template Email ID with content to send

    params: dict
        Parameters with data to include in mail

    subject_params: dict
        Parameters with data to include in mail subject

    receivers: list/str
        Email receiver/s
    
    tracking_dict: dict
        Contains the data of tracking and determine if the email will be tracking
    

    Return
    ------

    result: bool
        True if the email was send or False if it fails

    """
    # pylint: disable=no-member
    template = EmailTemplate.objects.filter(email_id=email_id).first()

    if not template:
        return False

    if isinstance(receivers, str):
        receivers = [receivers]

    if tracking_dict:
        for receiver in receivers:
            tracking = EmailTracking.objects.create(
                    receivers=receiver,
                    id_module=tracking_dict["id_module"],
                    type_module=tracking_dict["type_module"],
                    confirmation_token=get_random_string(16)
                )
            try:
                subject = template.subject.format(**subject_params)
                content = (
                    _HEADER_MESSAGE +
                    template.template.format(**params) +
                    _FOOTER_MESSAGE
                )
                tracking.subject = subject
                tracking.content = content
                tracking.save()
                html = (
                    f"<img src='{getenv('API_HOSTNAME')}/api/v1/email_tracking/"
                    f"{tracking.pk}/{tracking.confirmation_token}'>" +
                    content
                )
            
                send_mail(
                    subject,
                    None,
                    None,
                    [receiver],
                    html_message=html,
                )
            except Exception as error:
                print("EMAIL_ERROR:", repr(error), " | ", email_id)
                tracking.status = ERROR
                tracking.content = f"{email_id} - {repr(error)}"
                tracking.save()
                return False
    else:
        try:
            send_mail(
                template.subject.format(**subject_params),
                None,
                None,
                receivers,
                html_message=(
                    _HEADER_MESSAGE +
                    template.template.format(**params) +
                    _FOOTER_MESSAGE
                ),
            )
        except Exception as error:
            print("EMAIL_ERROR:", repr(error), " | ", email_id)
            return False
    return True
