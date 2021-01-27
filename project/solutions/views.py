import datetime
from random import randint

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.models import ClientProfile
from accounts.models import StaffProfile
from accounts.models import StudentProfile
from accounts.models import UserRegistration
from project.email import send_email
from solutions.forms import StaffForm
from solutions.forms import StudentForm
from solutions.models import ClientRequests
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
            form.save_user()
            return redirect('staff-create-list')
    else:
        form = StaffForm()
    return render(request, 'admin/staff_list.html', {'form': form, 'title': title, 'list_data': list_data})


@admin_required()
def student_create_list_view(request):
    title = 'Students'
    list_data = StudentProfile.objects.all()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save_user()
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
        messages.error(request, 'not found')
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
            message = f"Hi {cq.name},\n your request for {cq.get_service_display()} is approved"
            f". \nplease login using given credentials \n\n Username: {username}\n Password: {password}"
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
        send_email(
            subject="Your request is rejected",
            message=f'Sorry {cq.name} your request for {cq.get_service_display()} service is rejected',
            recipient_list=[cq.email, ]
        )
        return redirect('client-request-list')
