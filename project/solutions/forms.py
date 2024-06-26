from django import forms
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator

from accounts.models import phone_regex
from accounts.models import ProgrammingLanguages
from accounts.models import UserRegistration
from solutions.models import ClientRequests
from solutions.models import Comments
from solutions.models import Feedback
from solutions.models import JobAllocationRequest
from solutions.models import Leaves
from solutions.models import Service

alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabets characters are allowed.')


class UserForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = {
            'username',
            'first_name',
            'last_name',
            'address',
            'phone_number',
            'email'
        }

    username = forms.CharField()
    first_name = forms.CharField(validators=[alphanumeric])
    last_name = forms.CharField(validators=[alphanumeric])
    password = forms.CharField(widget=forms.PasswordInput())
    address = forms.TextInput()
    phone_number = forms.CharField(validators=[phone_regex])
    email = forms.EmailField()


def get_user_instance(data):
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    address = data.get('address')
    phone_number = data.get('phone_number')
    email = data.get('email')

    user = UserRegistration(username=username, first_name=first_name, last_name=last_name,
                            address=address, phone_number=phone_number, email=email)
    user.set_password(password)
    user.save()
    return user


class StaffForm(UserForm):
    position = forms.CharField()
    experience = forms.CharField()
    qualification = forms.CharField()
    salary = forms.CharField()
    skills = forms.CharField()

    def save_user(self):
        from accounts.models import StaffProfile
        user = get_user_instance(self.cleaned_data)
        user.is_staff = True
        user.save()
        position = self.cleaned_data.get('position')
        experience = self.cleaned_data.get('experience')
        qualification = self.cleaned_data.get('qualification')
        salary = self.cleaned_data.get('salary')
        skills = self.cleaned_data.get('skills')
        staff_profile = StaffProfile(user=user, position=position, experience=experience, qualification=qualification,
                                     salary=salary, skills=skills)
        staff_profile.save()
        return user


class StudentForm(UserForm):
    age = forms.IntegerField(validators=[MinValueValidator(0),
                                         MaxValueValidator(35)])
    college = forms.CharField()
    course = forms.ModelChoiceField(queryset=ProgrammingLanguages.objects.all())
    project_due_date = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    fees = forms.IntegerField()

    def save_user(self):
        from accounts.models import StudentProfile
        user = get_user_instance(self.cleaned_data)
        user.is_student = True
        user.save()
        age = self.cleaned_data.get('age')
        college = self.cleaned_data.get('college')
        course = self.cleaned_data.get('course')
        project_due_date = self.cleaned_data.get('project_due_date')
        fees = self.cleaned_data.get('fees')
        profile = StudentProfile(age=age, college=college, course=course, project_due_date=project_due_date, fees=fees,
                                 user=user)
        profile.save()
        return user


class ClientRequestForm(forms.ModelForm):
    class Meta:
        model = ClientRequests
        fields = {
            'message',
            'service',
        }


class LanguageForms(forms.ModelForm):
    class Meta:
        model = ProgrammingLanguages
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {'suggestion'}
        widgets = {
            'suggestion': forms.Textarea
        }


class JobAssignForm(forms.ModelForm):
    id_list = []
    try:
        job_requests = JobAllocationRequest.objects.filter(status='pending')
        for job in job_requests:
            id_list.append(job.service_id)
    except Exception as e:
        print(e)
        pass
    service_qs = Service.objects.filter(staff__isnull=True)
    service_qs = service_qs.exclude(id__in=id_list)
    staff = forms.ModelChoiceField(queryset=UserRegistration.objects.filter(is_staff=True, is_superuser=False))
    service = forms.ModelChoiceField(queryset=service_qs)

    class Meta:
        model = JobAllocationRequest
        fields = {
            'staff',
            'service',
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = {
            'feedback'
        }


class LeavesForm(forms.ModelForm):
    leave_type = forms.ChoiceField(choices=(('Sick', 'Sick'), ('Casual', 'Casual')))
    from_date = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    to_date = forms.DateTimeField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Leaves
        fields = {
            'from_date',
            'to_date',
            'reason',
            'leave_type',
            'comment',
        }


class ProjectDetailsUpdateForm(forms.ModelForm):
    due_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Service
        fields = {
            'name',
            'due_date'
        }
