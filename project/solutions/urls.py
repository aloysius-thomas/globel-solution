from django.urls import path

from solutions.views import client_list_view
from solutions.views import staff_create_list_view
from solutions.views import student_create_list_view

urlpatterns = [
    path('users/staff/', staff_create_list_view, name='staff-create-list'),
    path('users/student/', student_create_list_view, name='student-create-list'),
    path('users/client/', client_list_view, name='client-list'),
]
