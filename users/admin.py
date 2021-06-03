from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.utils.translation import gettext as _

from users.forms import TeacherForm, StudentForm
from users.models import User, Teacher, Student, Admin, AdminProfile


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'get_roles']

    def get_roles(self, user):
        return [role.get_id_display() for role in user.roles.all()]

    get_roles.short_description = 'Roles'
    get_roles.admin_order_field = 'id'

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}
         ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', "my_code.js",)

    def save_model(self, request, obj, form, change):
        valid = form.is_valid()
        if valid:
            data = form.cleaned_data
            dep = data.pop('department')
            st_class = data.pop('class')
            print(dep)
            print(st_class)
            # super(StudentAdmin, self).save_model(request, obj, form, change)
            # profile = obj.teacher_profile
            # profile.department = dep
            # profile.save()


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm

    def save_model(self, request, obj, form, change):
        valid = form.is_valid()
        if valid:
            data = form.cleaned_data
            dep = data.pop('department')
            super(TeacherAdmin, self).save_model(request, obj, form, change)
            profile = obj.teacher_profile
            profile.department = dep
            profile.save()


@admin.register(Admin)
class AdminAdmin(UserAdmin):

    def save_related(self, request, form, formsets, change):
        super(AdminAdmin, self).save_related(request, form, formsets, change)
        form.instance.roles.add(1)


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    pass
