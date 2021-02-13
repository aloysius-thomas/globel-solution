from django.contrib import admin

from accounts.models import ClientProfile
from accounts.models import ProgrammingLanguages
from accounts.models import StaffProfile
from accounts.models import StudentProfile
from accounts.models import TeachingSubjects
from accounts.models import UserRegistration

admin.site.register(UserRegistration)
admin.site.register(ProgrammingLanguages)
admin.site.register(StaffProfile)
admin.site.register(TeachingSubjects)
admin.site.register(StudentProfile)
admin.site.register(ClientProfile)
