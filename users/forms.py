from django import forms
from django.contrib.admin import site
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from university_app.admin import DepartmentAdmin
from university_app.models import Department, Class
from users.models import Teacher, Student


class TeacherForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    department = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        form = super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()

    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'email', 'password', 'department')


class StudentForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    department = forms.ModelChoiceField(queryset=None)
    st_class = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        form = super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()
        self.fields['st_class'].queryset = Class.objects.all()

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'password', 'department', 'st_class')
