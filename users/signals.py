from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import StudentProfile, User, Role, TeacherProfile

#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         roles = instance.roles.all()
#         teacher_role = Role.objects.get(id=Role.TEACHER)
#         student_role = Role.objects.get(id=Role.STUDENT)
#         if student_role in roles:
#             StudentProfile.objects.create(user=instance)
#         elif teacher_role in roles:
#             TeacherProfile.objects.create(user=instance)
#
#
# @receiver(post_delete, sender=User)
# def delete_user_profile(sender, instance, **kwargs):
#     roles = instance.roles.all()
#     if Role.STUDENT in roles:
#         instance.student_profile.save()
#     elif Role.TEACHER in roles:
#         instance.teacher_profile.save()
