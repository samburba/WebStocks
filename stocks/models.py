from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField('Owned_Stock', related_name='stocks', blank=True)
    #stocks = models.ManyToManyField('Owned_Stock', related_name='stocks', blank=True)
    purse = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    estimated_net = models.DecimalField(max_digits=64, decimal_places=2, null=True, default=1000)
    def __str__(self):
       return self.user.get_username()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Stock(models.Model):
    slug = models.SlugField(max_length=5)
    full_name = models.CharField(max_length=64, blank=True)
    bio = models.CharField(max_length=1024, null=True, blank=True)
    @permalink
    def get_absolute_url(self):
        return ('view_stock', None, { 'slug': self.name })
    def __str__(self):
       return self.slug

class Owned_Stock(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=64, decimal_places=2, null=True)
    purchased_date = models.DateTimeField(auto_now=True)
    def __str__(self):
       return self.user.user.get_username() + " : " + self.stock.slug

#Comments on stocks
class Comment(models.Model):
    stock = models.ForeignKey('Stock', related_name='stock', on_delete=models.CASCADE)
    text = models.CharField(max_length=141)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    authored = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.stock.slug + " : " + self.text
