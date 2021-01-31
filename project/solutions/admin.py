from django.contrib import admin

from solutions.models import Feedback
from accounts.models import StudentProfile
from solutions.models import Leaves
from solutions.models import Service

admin.site.register(Leaves)
admin.site.register(Feedback)
admin.site.register(StudentProfile)
admin.site.register(Service)
