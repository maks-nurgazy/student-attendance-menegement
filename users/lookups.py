from ajax_select import register, LookupChannel

from university_app.models import Class, Department


@register('classes')
class ClassesLookup(LookupChannel):
    model = Class

    def get_query(self, q, request):
        return self.model.objects.all()

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.num


@register('departments')
class ClassesLookup(LookupChannel):
    model = Department

    def get_query(self, q, request):
        profile = request.user.admin_profile
        university = profile.university
        faculties = university.faculties.all()
        departments = Department.objects.filter(faculty__in=faculties)
        departments = departments.filter(name__icontains=q)
        return departments

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name
