from django.urls import path, include
from rest_framework.routers import DefaultRouter

from university_app.api.views import FacultyViewSet, DepartmentViewSet, UniversityViewSet, ClassViewSet

university = DefaultRouter()
university.register('universities', UniversityViewSet)

faculty = DefaultRouter()
faculty.register('faculties', FacultyViewSet)

departments = DefaultRouter()
departments.register('departments', DepartmentViewSet, basename='departments')

classes = DefaultRouter()
classes.register('classes', ClassViewSet, basename='classes')

urlpatterns = [
    path('', include((university.urls, 'university_app'), namespace='university')),
    path('', include((faculty.urls, 'university_app'), namespace='faculty')),
    path('faculties/<int:faculty_id>/',
         include((departments.urls, 'university_app'), namespace='departments')),
    path('departments/<int:department_id>/',
         include((classes.urls, 'university_app'), namespace='classes')),

]
