from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.models import ClientProfile
from accounts.models import StaffProfile
from accounts.models import StudentProfile
from solutions.forms import ClientRequestForm
from solutions.forms import StaffForm
from solutions.forms import StudentForm
from solutions.models import ClientRequests


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
