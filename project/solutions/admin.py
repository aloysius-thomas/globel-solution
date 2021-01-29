from django.contrib import admin

from solutions.models import Feedback
from accounts.models import StudentProfile
from solutions.models import Leaves

admin.site.register(Leaves)
admin.site.register(Feedback)
admin.site.register(StudentProfile)
