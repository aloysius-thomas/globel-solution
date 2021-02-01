from django.urls import path

from solutions.views import accept_job
from solutions.views import approve_client_request_view
from solutions.views import approve_leave_request
from solutions.views import assign_job
from solutions.views import client_list_view
from solutions.views import client_request_list
from solutions.views import client_request_success_view
from solutions.views import client_request_view
from solutions.views import comment_project_view
from solutions.views import feedback_list_view
from solutions.views import job_allocations_for_staff
from solutions.views import mark_absent
from solutions.views import mark_attendance
from solutions.views import month_wise_attendance_list
from solutions.views import my_projects
from solutions.views import my_projects_staff
from solutions.views import programing_languages_create_list_view
from solutions.views import programing_languages_delete_view
from solutions.views import project_make_finished
from solutions.views import project_update_status
from solutions.views import reject_client_request_view
from solutions.views import reject_job
from solutions.views import reject_leave_request
from solutions.views import request_leave
from solutions.views import request_service
from solutions.views import service_detail_view
from solutions.views import service_list_view
from solutions.views import staff_create_list_view
from solutions.views import staff_leave_request_list
from solutions.views import student_create_list_view
from solutions.views import student_leave_request_list
from solutions.views import students_attendance
from solutions.views import update_profile_details
from solutions.views import write_feedback

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
    path('service/<int:service_id>/update/', update_profile_details, name='service-update-view'),
    path('service/<int:service_id>/update-status/', project_update_status, name='service-update-status-view'),
    path('service/<int:service_id>/finished/', project_make_finished, name='service-finished-view'),
    path('comment/<int:project_id>/', comment_project_view, name='comment-project-view'),
    path('assign-jobs/', assign_job, name='assign-jobs'),
    path('feedback/', write_feedback, name='feedback'),
    path('my-projects/', my_projects, name='my-projects'),
    path('request-leave/', request_leave, name='request-leave'),
    path('request-service/', request_service, name='request-service'),
    path('staff/job-requests/', job_allocations_for_staff, name='staff-job-requests'),
    path('staff/job-requests/accept/<int:job_id>/', accept_job, name='staff-job-accept'),
    path('staff/job-requests/reject/<int:job_id>/', reject_job, name='staff-job-reject'),
    path('staff/my-project/', my_projects_staff, name='staff-my-projects'),
    path('staff/students-attendance/', students_attendance, name='staff-students-attendance'),
    path('staff/mark-attendance/<int:obj_id>/', mark_attendance, name='staff-mark-attendance'),
    path('staff/mark-absent/<int:obj_id>/', mark_absent, name='staff-mark-absent'),
    path('admin/staff-leave-request/list/', staff_leave_request_list, name='staff-leave-request-list'),
    path('admin/student-leave-request/list/', student_leave_request_list, name='student-leave-request-list'),
    path('admin/leave-request/<int:obj_id>/approve/', approve_leave_request, name='staff-leave-request-approve'),
    path('admin/leave-request/<int:obj_id>/reject/', reject_leave_request, name='staff-leave-request-reject'),
    path('admin/feedback/', feedback_list_view, name='feedback-list'),
    path('attendance/<int:month>/<int:year>/<user_id>/', month_wise_attendance_list,
         name='month-wise-attendance-list'),
]
