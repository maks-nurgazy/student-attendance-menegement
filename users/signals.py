from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User


# @receiver(request_finished, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     print(kwargs)
#     if created:
#         print(kwargs)

# @receiver(post_delete, sender=User)
# def delete_user_profile(sender, instance, **kwargs):
#     roles = instance.roles.all()
#     if Role.STUDENT in roles:
#         instance.student_profile.save()
#     elif Role.TEACHER in roles:
#         instance.teacher_profile.save()
