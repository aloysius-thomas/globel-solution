from django.urls import path

from solutions.views import approve_client_request_view
from solutions.views import client_list_view
from solutions.views import client_request_list
from solutions.views import client_request_success_view
from solutions.views import client_request_view
from solutions.views import comment_project_view
from solutions.views import programing_languages_create_list_view
from solutions.views import programing_languages_delete_view
from solutions.views import reject_client_request_view
from solutions.views import service_detail_view
from solutions.views import service_list_view
from solutions.views import staff_create_list_view
from solutions.views import student_create_list_view

urlpatterns = [
    path('client-request/success/', client_request_success_view, name='client-request-success'),
    path('client-request/', client_request_view, name='client-request-create'),
    path('users/staff/', staff_create_list_view, name='staff-create-list'),
    path('users/student/', student_create_list_view, name='student-create-list'),
    path('users/client/', client_list_view, name='client-list'),
    path('client-requests/', client_request_list, name='client-request-list'),
    path('client-requests/<int:request_id>/accept/', approve_client_request_view, name='client-request-accept'),
    path('client-requests/<int:request_id>/reject/', reject_client_request_view, name='client-request-reject'),
    path('programing-languages', programing_languages_create_list_view, name='programing-languages-create-list-view'),
    path('programing-languages/<int:pl_id>/delete/', programing_languages_delete_view,
         name='programing-languages-delete-view'),
    path('service/<str:service>/', service_list_view, name='service-list-view'),
    path('service/<int:service_id>/details/', service_detail_view, name='service-details-view'),
    path('comment/<int:project_id>/', comment_project_view, name='comment-project-view'),
]
