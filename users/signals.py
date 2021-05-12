from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import StudentProfile, User, Role, TeacherProfile


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        roles = instance.roles.all()
        if Role.STUDENT in roles:
            StudentProfile.objects.create(user=instance)
        elif Role.TEACHER in roles:
            TeacherProfile.objects.create(user=instance)


@receiver(post_delete, sender=User)
def delete_student_profile(sender, instance, **kwargs):
    roles = instance.roles.all()
    if Role.STUDENT in roles:
        instance.student_profile.save()
    elif Role.TEACHER in roles:
        instance.teacher_profile.save()
