from django.contrib import admin

from solutions.models import Attendance
from solutions.models import ClientRequests
from solutions.models import Comments
from solutions.models import Feedback
from solutions.models import JobAllocationRequest
from solutions.models import Leaves
from solutions.models import Notify
from solutions.models import Service

admin.site.register(ClientRequests)
admin.site.register(Service)
admin.site.register(Comments)
admin.site.register(Notify)
admin.site.register(Attendance)
admin.site.register(Leaves)
admin.site.register(JobAllocationRequest)
admin.site.register(Feedback)
