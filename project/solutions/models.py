from django.db import models

from accounts.models import phone_regex
from accounts.models import SERVICES
from accounts.models import STATUS
from accounts.models import UserRegistration


class ClientRequests(models.Model):
    client = models.ForeignKey(on_delete=models.CASCADE, to=UserRegistration, blank=True, null=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(default='example@email.com')
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    message = models.TextField()
    service = models.CharField(choices=SERVICES, max_length=32)
    status = models.CharField(choices=STATUS, max_length=32, default='pending')

    def __str__(self):
        string = f'Client Request'
        if self.client:
            string = f'Client Request of {self.client}'
        return string


class Service(models.Model):
    service = models.CharField(choices=SERVICES, max_length=32)
    name = models.CharField(max_length=128, blank=True, null=True)
    client = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='service_client')
    staff = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='service_staff', blank=True,
                              null=True)
    start_date = models.DateField()
    finished = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=100)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=32, default='Project Started')
    status_updated_on = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_service_display()} of {self.client.get_full_name()}'


class Comments(models.Model):
    commented_by = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    projects = models.ForeignKey(Service, on_delete=models.CASCADE, )
    suggestion = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.projects} by {self.commented_by}'


class Notify(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    notification = models.CharField(max_length=256)

    def __str__(self):
        return f'Notification For {self.user}'


class Attendance(models.Model):
    ATTENDANCE_STATUS = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('pending', 'Pending'),
    )
    user = models.ForeignKey(to=UserRegistration, on_delete=models.CASCADE)
    status = models.CharField(choices=ATTENDANCE_STATUS, max_length=32, default='pending')
    date = models.DateField()

    def __str__(self):
        return f'{self.user}-{self.date}'


class Leaves(models.Model):
    taken_by = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=10)
    leave_type = models.CharField(max_length=10)
    comment = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=32, default='pending')

    def __str__(self):
        return f'Leave request of {self.taken_by}'


class JobAllocationRequest(models.Model):
    staff = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=32, default='pending')
    created_on = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        return f'Job allocation {self.service} for {self.staff}'


class Feedback(models.Model):
    user = models.ForeignKey(to=UserRegistration, on_delete=models.CASCADE)
    feedback = models.TextField()
    added_on = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'User feedback {self.user}'
