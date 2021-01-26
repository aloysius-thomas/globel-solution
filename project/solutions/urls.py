from django.urls import path

from solutions.views import staff_create_list_view

urlpatterns = [
    path('users/staff/', staff_create_list_view, name='staff-create-list'),
]
