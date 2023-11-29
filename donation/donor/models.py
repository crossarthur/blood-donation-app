from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# Create your models here.


class BloodTypes(models.Model):
    name = models.CharField(max_length=20)
    pint = models.IntegerField(default=0)

    def __str__(self):
        return self.name


STATUS = (
    ('Pending', 'Pending'),
    ('Rejected', 'Rejected'),
    ('Accepted', 'Accepted'),
)

sex = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class Request(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    sex = models.CharField(max_length=20, choices=sex, default= 'Male')
    age = models.IntegerField()
    blood = models.ForeignKey(BloodTypes, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    pint = models.IntegerField()
    status = models.CharField(max_length=25, choices=STATUS, default='Pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.username


Blood_Type = (
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB-', 'AB-'),
    ('AB+', 'AB+'),

)


class Donor(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    sex = models.CharField(max_length=20, choices=sex, default='Male', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    blood = models.ForeignKey(BloodTypes, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    pint = models.IntegerField()

    def __str__(self):
        return self.name.username


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uname', default='0')
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='image/')
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=20, choices=sex)


@receiver(post_save, sender=User)
def profile(sender, created, instance, **kwargs):
    if created:
        new_profile = Profile(user=instance)
        new_profile.save()

