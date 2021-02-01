import datetime
from random import randint

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.models import ClientProfile
from accounts.models import ProgrammingLanguages
from accounts.models import StaffProfile
from accounts.models import StudentProfile
from accounts.models import UserRegistration
from project.email import send_email
from solutions.forms import ClientRequestForm
from solutions.forms import CommentForm
from solutions.forms import FeedbackForm
from solutions.forms import JobAssignForm
from solutions.forms import LanguageForms
from solutions.forms import LeavesForm
from solutions.forms import ProjectDetailsUpdateForm
from solutions.forms import StaffForm
from solutions.forms import StudentForm
from solutions.models import Attendance
from solutions.models import ClientRequests
from solutions.models import Comments
from solutions.models import Feedback
from solutions.models import JobAllocationRequest
from solutions.models import Leaves
from solutions.models import Service


def admin_required(login_url='login'):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)


@admin_required()
def staff_create_list_view(request):
    title = 'Staff'
    list_data = StaffProfile.objects.all()
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            user = form.save_user()
            messages.success(request, 'Staff account created successfully')
            send_email(
                subject="Your Account is created",
                message=f"Hi {first_name} {last_name}\n Yor staff account is created. Please login using given credentials\n Username: {username}\n Password: {password} ",
                recipient_list=[user.email, ]
            )
            return redirect('staff-create-list')
    else:
        form = StaffForm()
    return render(request, 'admin/staff_list.html', {'form': form, 'title': title, 'list_data': list_data})


@admin_required()
def student_create_list_view(request):
    title = 'Students'
    list_data = StudentProfile.objects.all().order_by('-id')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            user = form.save_user()
            messages.success(request, 'Student account created successfully')
            send_email(
                subject="Your Account is created",
                message=f"Hi Student \n Yor account is created. Please login using given credentials\n Username: {username}\n Password: {password} ",
                recipient_list=[user.email, ]
            )
            return redirect('student-create-list')
    else:
        form = StudentForm()
    return render(request, 'admin/student_list.html', {'form': form, 'title': title, 'list_data': list_data})


@admin_required()
def client_list_view(request):
    title = 'Clients'
    list_data = ClientProfile.objects.all()
    return render(request, 'admin/client_list.html', {'title': title, 'list_data': list_data})


def client_request_view(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)
        phone_number = request.GET.get('phone_number', None)
        service = request.GET.get('service', None)
        message = request.GET.get('message', None)
        if name and email and phone_number and service and message:
            ClientRequests.objects.create(name=name, email=email, phone_number=phone_number, service=service,
                                          message=message)

        return redirect('client-request-success')


def client_request_success_view(request):
    return render(request, 'client_request_success.html')


@admin_required()
def client_request_list(request):
    pending = ClientRequests.objects.filter(status='pending')
    approved = ClientRequests.objects.filter(status='approved')
    rejected = ClientRequests.objects.filter(status='rejected')
    title = 'Client Requests'
    context = {
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'title': title
    }
    return render(request, 'admin/client_request_list.html', context)


@admin_required()
def approve_client_request_view(request, request_id):
    try:
        cq = ClientRequests.objects.get(id=request_id)
    except ClientRequests.DoesNotExist:
        return HttpResponseNotFound()
    else:
        import random
        import string
        if cq.client is None:
            password = ''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=6))

            username = cq.name.replace(" ", "-")
            while True:
                if UserRegistration.objects.filter(username=username).exists():
                    username = username + str(randint(0, 9))
                else:
                    break
            client = UserRegistration(username=username, phone_number=cq.phone_number, address='not provided',
                                      email=cq.email, first_name=cq.name)
            client.set_password(password)
            client.save()
            profile = ClientProfile.objects.create(user=client, service=cq.service)
            profile.save()
            cq.client = client
            cq.save()
            message = f"Hi {cq.name},\n your request for {cq.get_service_display()} is approved. \n please login using given credentials \n\n Username: {username}\n Password: {password}"
        else:
            message = f"Hi {cq.name},\n your request for {cq.get_service_display()} is approved\nplease login using your user name and password"

        service = Service.objects.create(service=cq.service, client=cq.client, start_date=datetime.datetime.now())
        service.save()
        cq.status = 'approved'
        cq.save()
        send_email(
            subject="Your request is accepted",
            message=message,
            recipient_list=[service.client.email, ]
        )
        messages.success(request, 'Request accepted and email send')
        return redirect('client-request-list')


@admin_required()
def reject_client_request_view(request, request_id):
    try:
        cq = ClientRequests.objects.get(id=request_id)
    except ClientRequests.DoesNotExist:
        messages.error(request, 'not found')
    else:
        cq.status = 'rejected'
        cq.save()
        messages.error(request, "Request Rejected")
        send_email(
            subject="Your request is rejected",
            message=f'Sorry {cq.name} your request for {cq.get_service_display()} service is rejected',
            recipient_list=[cq.email, ]
        )
        return redirect('client-request-list')


@admin_required()
def programing_languages_create_list_view(request):
    title = 'Programing Languages (Courses)'
    list_data = ProgrammingLanguages.objects.all()
    if request.method == 'POST':
        form = LanguageForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added")
            return redirect('programing-languages-create-list-view')
    else:
        form = LanguageForms()
    return render(request, 'admin/programming_language_list.html',
                  {'form': form, 'title': title, 'list_data': list_data})


@admin_required()
def programing_languages_delete_view(request, pl_id):
    try:
        pl = ProgrammingLanguages.objects.get(id=pl_id)
    except ProgrammingLanguages.DoesNotExist:
        messages.error(request, 'Not found')
        return redirect('programing-languages-create-list-view')
    else:
        pl.delete()
        messages.error(request, "Deleted")
        return redirect('programing-languages-create-list-view')


@admin_required()
def service_list_view(request, service):
    temp = service.replace("-", " ")
    title = f'{temp.title()} Service'
    data = Service.objects.filter(service=service)
    return render(request, 'admin/services_list.html', {'title': title, 'data': data})


@login_required
def service_detail_view(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    if not service.due_date or not service.name:
        return redirect('service-update-view', service.id)
    comments = Comments.objects.filter(projects=service)
    form = CommentForm()
    return render(request, 'admin/services_details.html', {'service': service, 'comments': comments, 'form': form})


@login_required()
def comment_project_view(request, project_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.commented_by = request.user
        comment.projects_id = project_id
        comment.save()
        return redirect('service-details-view', project_id)


@admin_required()
def assign_job(request):
    title = 'Assign Jobs'
    list_data = JobAllocationRequest.objects.all().order_by('-id')
    if request.method == 'POST':
        form = JobAssignForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job added successfully")
            return redirect('assign-jobs')
    else:
        form = JobAssignForm()
    return render(request, 'admin/job_assign_list.html', {'form': form, 'title': title, 'list_data': list_data})


@login_required()
def write_feedback(request):
    title = 'Write a Feedback'
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Success')
            return redirect('dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'admin/feedback_create.html', {'form': form, 'title': title})


@login_required()
def my_projects(request):
    title = 'My Projects'
    data = Service.objects.filter(client=request.user)
    return render(request, 'admin/services_list.html', {'title': title, 'data': data})


@login_required()
def request_leave(request):
    title = 'Request Leave'
    data = Leaves.objects.filter(taken_by=request.user)
    if request.method == 'POST':
        form = LeavesForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.taken_by = request.user
            leave.save()
            messages.success(request, 'Success')
            return redirect('request-leave')
    else:
        form = LeavesForm()
    return render(request, 'admin/leave-create.html', {'form': form, 'title': title, 'list_data': data})


@login_required()
def request_service(request):
    title = 'Request Service'
    if request.method == 'POST':
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = request.user
            obj.name = request.user.first_name
            obj.email = request.user.email
            obj.phone_number = request.user.phone_number
            obj.save()
            messages.success(request, 'Success')
            return redirect('my-projects')
    else:
        form = ClientRequestForm()
    return render(request, 'admin/request-service.html', {'form': form, 'title': title})


@login_required
def job_allocations_for_staff(request):
    pending = JobAllocationRequest.objects.filter(status='pending', staff=request.user)
    approved = JobAllocationRequest.objects.filter(status='approved', staff=request.user)
    rejected = JobAllocationRequest.objects.filter(status='rejected', staff=request.user)
    title = 'Job Assignments'
    context = {
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'title': title
    }
    return render(request, 'staff/job-list.html', context)


@login_required
def accept_job(request, job_id):
    try:
        job = JobAllocationRequest.objects.get(id=job_id)
    except JobAllocationRequest.DoesNotExist:
        return HttpResponseNotFound('Not Found')
    else:
        job.status = 'approved'
        job.save()
        job.service.staff = request.user
        job.service.save()
        return redirect('staff-job-requests')


@login_required
def reject_job(request, job_id):
    try:
        job = JobAllocationRequest.objects.get(id=job_id)
    except JobAllocationRequest.DoesNotExist:
        return HttpResponseNotFound('Not Found')
    else:
        job.status = 'rejected'
        job.save()
        return redirect('staff-job-requests')


@login_required()
def my_projects_staff(request):
    title = 'My Projects'
    data = Service.objects.filter(staff=request.user)
    return render(request, 'admin/services_list.html', {'title': title, 'data': data})


@login_required()
def students_attendance(request):
    today = datetime.datetime.now().date()
    title = f'Student Attendance of {today}'
    if not Attendance.objects.filter(date=today).exists():
        students = UserRegistration.objects.filter(is_student=True)
        for student in students:
            Attendance.objects.create(user=student, date=today)

    pending = Attendance.objects.filter(date=today, status='pending')
    attendance = Attendance.objects.filter(date=today, status__in=['present', 'absent'])

    return render(request, 'staff/attendance.html',
                  {'pending': pending, 'title': title, 'attendance': attendance, 'month': today.month,
                   'year': today.year})


@login_required
def mark_attendance(request, obj_id):
    try:
        attendance = Attendance.objects.get(id=obj_id)
    except Attendance.DoesNotExist:
        return HttpResponseNotFound('Not Found')
    else:
        attendance.status = 'present'
        attendance.save()
        return redirect('staff-students-attendance')


@login_required
def mark_absent(request, obj_id):
    try:
        attendance = Attendance.objects.get(id=obj_id)
    except Attendance.DoesNotExist:
        return HttpResponseNotFound('Not Found')
    else:
        attendance.status = 'absent'
        attendance.save()
        return redirect('staff-students-attendance')


@admin_required()
def staff_leave_request_list(request):
    title = 'Staff Leave Requests'
    list_data = Leaves.objects.filter(taken_by__is_staff=True, status='pending')
    approved = Leaves.objects.filter(taken_by__is_staff=True, status='approved')
    rejected = Leaves.objects.filter(taken_by__is_staff=True, status='rejected')
    context = {'title': title, 'list_data': list_data, 'approved': approved, 'rejected': rejected}
    return render(request, 'admin/leave_list.html', context)


@admin_required()
def student_leave_request_list(request):
    title = 'Staff Leave Requests'
    list_data = Leaves.objects.filter(taken_by__is_student=True, status='pending')
    approved = Leaves.objects.filter(taken_by__is_student=True, status='approved')
    rejected = Leaves.objects.filter(taken_by__is_student=True, status='rejected')
    context = {'title': title, 'list_data': list_data, 'approved': approved, 'rejected': rejected}

    return render(request, 'admin/leave_list.html', context)


@login_required
def approve_leave_request(request, obj_id):
    try:
        leave = Leaves.objects.get(id=obj_id)
    except Leaves.DoesNotExist:
        return HttpResponseNotFound('Not Found')
    else:
        leave.status = 'approved'
        leave.save()
        messages.success(request, 'Leave Approved')
        if leave.taken_by.is_staff:
            url = redirect('staff-leave-request-list')
        else:
            url = redirect('student-leave-request-list')
        return url


@login_required
def reject_leave_request(request, obj_id):
    try:
        leave = Leaves.objects.get(id=obj_id)
    except Leaves.DoesNotExist:
        return HttpResponseNotFound('Not Found')
    else:
        leave.status = 'rejected'
        leave.save()
        messages.error(request, 'Leave Rejected')
        if leave.taken_by.is_staff:
            url = redirect('staff-leave-request-list')
        else:
            url = redirect('student-leave-request-list')
        return url


@login_required
def feedback_list_view(request):
    feedback_list = Feedback.objects.all().order_by('-id')
    context = {'title': 'Feedback', 'feedback_list': feedback_list}
    return render(request, 'admin/feedback_list.html', context)


@login_required
def month_wise_attendance_list(request, month=0, year=0, user_id='all'):
    import calendar
    this_month = datetime.datetime.now().month
    this_year = datetime.datetime.now().year
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    students = UserRegistration.objects.filter(is_student=True)
    attendance = Attendance.objects.all()
    if month and year:
        attendance = attendance.filter(date__month=month, date__year=year)
        last_day_of_month = calendar.monthrange(int(year), int(month))[1]

    else:
        attendance = attendance.filter(date__month=this_month, date__year=this_year)
        last_day_of_month = calendar.monthrange(int(this_year), int(this_month))[1]
    student_name = None
    month_days = [i + 1 for i in range(last_day_of_month)]
    if user_id != 'all':
        attendance = attendance.filter(user_id=request.user.id)
        if attendance:
            student_name = attendance.last().user
        days = {i + 1: 'Not marked' for i in range(last_day_of_month)}
        for day in attendance:
            days.update({day.date.day: day.get_status_display()})
        attendance = days
    else:
        data = {}
        temp_attendance = attendance
        for student in students:
            months = temp_attendance.filter(user=student)
            days = {i + 1: 'Not marked' for i in range(last_day_of_month)}
            for date in months:
                days.update({date.date.day: date.status})

            data.update({student.id: {'name': student.get_full_name(), 'status': days}})
            attendance = data

    context = {
        'attendance': attendance,
        'student': student_name,
        'month': month if month else this_month,
        'year': year if year else this_year,
        'month_days': month_days,
        'range': len(month_days),
        'next_month': next_month,
        'next_year': next_year,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'this_month': this_month,
        'this_year': this_year,
    }
    return render(request, 'admin/month-wise-attendance.html', context)


@login_required
def update_profile_details(request, service_id):
    try:
        project = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return HttpResponseNotFound()
    else:
        if request.method == 'POST':
            form = ProjectDetailsUpdateForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                messages.success(request, 'Project Updated')
                return redirect('service-details-view', project.id)
        else:
            form = ProjectDetailsUpdateForm(instance=project)
        return render(request, 'admin/services_update.html', {'form': form})


@login_required
def project_make_finished(request, service_id):
    try:
        project = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return HttpResponseNotFound()
    else:
        project.finished = datetime.datetime.now().date()
        project.status = "Work Finished"
        project.save()
    return redirect('service-details-view', project.id)


def project_update_status(request, service_id):
    try:
        project = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return HttpResponseNotFound()
    else:
        project.status = request.POST.get('status')
        project.save()
    return redirect('service-details-view', project.id)
