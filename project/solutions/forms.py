from django import forms

from accounts.models import phone_regex
from accounts.models import ProgrammingLanguages
from accounts.models import UserRegistration
from solutions.models import ClientRequests
from solutions.models import Comments
from solutions.models import Feedback
from solutions.models import JobAllocationRequest
from solutions.models import Leaves


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
    first_name = forms.CharField()
    last_name = forms.CharField()
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
    age = forms.CharField()
    college = forms.CharField()
    course = forms.ModelChoiceField(queryset=ProgrammingLanguages.objects.all())
    project_due_date = forms.DateField()
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
    staff = forms.ModelChoiceField(queryset=UserRegistration.objects.filter(is_staff=True, is_superuser=False))

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

    class Meta:
        model = Leaves
        fields = {
            'from_date',
            'to_date',
            'reason',
            'leave_type',
            'comment',
        }
