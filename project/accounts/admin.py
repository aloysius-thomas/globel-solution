from django.contrib import admin

from accounts.models import UserRegistration
from solutions.models import ClientRequests

admin.site.register(ClientRequests)
admin.site.register(UserRegistration)
