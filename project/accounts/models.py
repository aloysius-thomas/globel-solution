from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message=
                             "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

SERVICES = (
    ('web-design', 'Web Design'),
    ('web-development', 'Web Development'),
    ('graphic-design', 'Graphic Design'),
    ('application-development', 'Application Development'),
    ('advertisement-creation', 'Advertisement Creation'),
    ('digital-marketing', 'Advertisement'),
    ('project-support', 'Project Support'),
)

STATUS = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)


class UserRegistration(AbstractUser):
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    address = models.TextField()
    is_client = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class ProgrammingLanguages(models.Model):
    name = models.CharField(max_length=126)


class StaffProfile(models.Model):
    user = models.OneToOneField(to=UserRegistration, on_delete=models.CASCADE)
    position = models.CharField(max_length=256)
    experience = models.CharField(max_length=256)
    qualification = models.CharField(max_length=256)
    salary = models.CharField(max_length=256)
    skills = models.CharField(max_length=256)


class TeachingSubjects(models.Model):
    teacher = models.ForeignKey(to=UserRegistration, on_delete=models.CASCADE)
    language = models.ForeignKey(to=ProgrammingLanguages, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['teacher', 'language']


class StudentProfile(models.Model):
    user = models.OneToOneField(UserRegistration, on_delete=models.CASCADE)
    age = models.CharField(max_length=2)
    college = models.CharField(max_length=128)
    course = models.ForeignKey(to=ProgrammingLanguages, on_delete=models.CASCADE)
    project_due_date = models.DateField()
    fees = models.IntegerField()


class ClientProfile(models.Model):
    user = models.ForeignKey(to=UserRegistration, on_delete=models.CASCADE)
    service = models.CharField(choices=SERVICES, max_length=32)

