# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from course_app.models import Course
#
#
# @receiver(post_save, sender=Course)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         user = instance.teacher
#         profile = user.teacher_profile
#         department = instance.co_class.department
#         profile.department_id = department
#         profile.save()
