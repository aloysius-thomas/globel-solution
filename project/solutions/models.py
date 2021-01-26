from django.db import models

from accounts.models import phone_regex
from accounts.models import SERVICES
from accounts.models import UserRegistration


class ClientRequests(models.Model):
    client = models.ForeignKey(on_delete=models.CASCADE, to=UserRegistration)
    name = models.CharField(max_length=150)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    message = models.TextField()
    service = models.CharField(choices=SERVICES, max_length=32)
    status = models.CharField(choices=SERVICES, max_length=32)


class Service(models.Model):
    service = models.CharField(choices=SERVICES, max_length=32)
    client = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='service_client')
    staff = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='service_staff')
    start_date = models.DateField()
    finished = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=100)
    status_updated_on = models.DateField(auto_now=True)


class Comments(models.Model):
    commented_by = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    projects = models.ForeignKey(Service, on_delete=models.CASCADE, )
    suggestion = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)


class Notify(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    notification = models.CharField(max_length=256)


class StudentAttend(models.Model):
    student_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, blank=True, null=True)
    attend_per = models.CharField(max_length=10)


class Leaves(models.Model):
    taken_by = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=10)
    leave_type = models.CharField(max_length=10)
    comment = models.CharField(max_length=50, blank=True, null=True)


class JobAllocationRequest(models.Model):
    staff = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
    status = models.CharField(choices=SERVICES, max_length=32)
    created_on = models.DateTimeField(auto_now_add=True)
