from django.urls import path, include
from rest_framework.routers import DefaultRouter

from university_app.api.views import FacultyViewSet, DepartmentViewSet, UniversityView, ClassViewSet

university = DefaultRouter()
university.register('faculties', FacultyViewSet)

departments = DefaultRouter()
departments.register('departments', DepartmentViewSet, basename='departments')

classes = DefaultRouter()
classes.register('classes', ClassViewSet, basename='classes')

urlpatterns = [
    path('university/', UniversityView.as_view()),
    path('university/', include((university.urls, 'university_app'), namespace='university')),
    path('university/faculties/<int:faculty_id>/',
         include((departments.urls, 'university_app'), namespace='departments')),
    path('departments/<int:department_id>/',
         include((classes.urls, 'university_app'), namespace='classes')),

]
