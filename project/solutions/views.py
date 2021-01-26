from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.models import ClientProfile
from accounts.models import StaffProfile
from accounts.models import StudentProfile
from solutions.forms import StaffForm
from solutions.forms import StudentForm


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
