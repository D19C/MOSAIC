from django.contrib import admin
from base.models.email_template import EmailTemplate
from base.models.email_tracking import EmailTracking
from base.models.environment_variables import EnvironmentVariables
from base.models.creator import Creator
from base.models.admin import Admin
from base.models.user import User

# Register your models here.
admin.site.register(Creator)
admin.site.register(Admin)
admin.site.register(User)
admin.site.register(EmailTemplate)
admin.site.register(EmailTracking)
admin.site.register(EnvironmentVariables)
