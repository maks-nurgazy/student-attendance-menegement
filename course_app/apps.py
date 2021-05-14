from django.apps import AppConfig


class CourseAppConfig(AppConfig):
    name = 'course_app'

    def ready(self):
        import course_app.signals
