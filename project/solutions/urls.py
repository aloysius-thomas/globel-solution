from django.urls import path

from solutions.views import approve_client_request_view
from solutions.views import client_list_view
from solutions.views import client_request_list
from solutions.views import client_request_success_view
from solutions.views import client_request_view
from solutions.views import staff_create_list_view
from solutions.views import student_create_list_view

urlpatterns = [
    path('client-request/success/', client_request_success_view, name='client-request-success'),
    path('client-request/', client_request_view, name='client-request-create'),
    path('users/staff/', staff_create_list_view, name='staff-create-list'),
    path('users/student/', student_create_list_view, name='student-create-list'),
    path('users/client/', client_list_view, name='client-list'),
    path('client-requests/', client_request_list, name='client-request-list'),
    path('client-requests/accept/', approve_client_request_view, name='client-request-accept'),
]
