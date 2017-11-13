from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField('stocks.Stocks', related_name='stocks', blank=True, null=True)
    purse = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Stocks(models.Model):
    name = models.SlugField(max_length=5)
    full_name = models.CharField(max_length=64)
    @permalink
    def get_absolute_url(self):
        return ('view_stock', None, { 'slug': self.name })
