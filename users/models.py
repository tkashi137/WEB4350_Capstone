from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
# user model added - Jami
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    funds = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

