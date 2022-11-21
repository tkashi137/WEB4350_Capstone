from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#user model added - Jami
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   # image = models.ImageField(default='profilepic.jpg', upload_to='profile_pictures') - won't work with heroku
    
    def __str__(self):
        return self.user.username

#may need date account created, 
