from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import Student, StudentProfile, User, Role


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)


@receiver(post_delete, sender=User)
def save_student_profile(sender, instance, **kwargs):
    instance.profile.save()
