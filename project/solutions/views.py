from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.models import UserRegistration
from solutions.forms import StaffForm


def admin_required(login_url='login'):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)


@admin_required()
def staff_create_list_view(request):
    title = 'Staff'
    list_data = UserRegistration.objects.filter(is_staff=True)
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save_user()
            return redirect('staff-create-list')
    else:
        form = StaffForm()
    return render(request, 'admin/staff_list.html', {'form': form, 'title': title, 'list_data': list_data})
