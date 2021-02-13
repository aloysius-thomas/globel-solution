from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

SERVICES = (
    ('web-design', 'Web Design'),
    ('web-development', 'Web Development'),
    ('graphic-design', 'Graphic Design'),
    ('application-development', 'Application Development'),
    ('advertisement-creation', 'Advertisement Creation'),
    ('digital-marketing', 'Digital Marketing'),
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

    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.username


class ProgrammingLanguages(models.Model):
    name = models.CharField(max_length=126)

    def __str__(self):
        return self.name


class StaffProfile(models.Model):
    user = models.OneToOneField(to=UserRegistration, on_delete=models.CASCADE)
    position = models.CharField(max_length=256)
    experience = models.CharField(max_length=256)
    qualification = models.CharField(max_length=256)
    salary = models.CharField(max_length=256)
    skills = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.user} Profile'


class TeachingSubjects(models.Model):
    teacher = models.ForeignKey(to=UserRegistration, on_delete=models.CASCADE)
    language = models.ForeignKey(to=ProgrammingLanguages, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['teacher', 'language']

    def __str__(self):
        return f'{self.user} Profile'


class StudentProfile(models.Model):
    user = models.OneToOneField(UserRegistration, on_delete=models.CASCADE)
    age = models.CharField(max_length=2)
    college = models.CharField(max_length=128)
    course = models.ForeignKey(to=ProgrammingLanguages, on_delete=models.CASCADE)
    project_due_date = models.DateField()
    fees = models.IntegerField()

    def __str__(self):
        return f'{self.user} Profile'


@receiver(post_save, sender=StudentProfile)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        from solutions.models import Service
        from datetime import datetime
        Service.objects.create(service='project-support', client=instance.user, start_date=datetime.now())


class ClientProfile(models.Model):
    user = models.ForeignKey(to=UserRegistration, on_delete=models.CASCADE)
    service = models.CharField(choices=SERVICES, max_length=32)

    def __str__(self):
        return f'{self.user} Profile'
