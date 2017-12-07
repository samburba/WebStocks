from django.contrib import admin
from stocks.models import Profile, Stock, Owned_Stock, Comment

admin.site.register(Profile)
admin.site.register(Stock)
admin.site.register(Owned_Stock)
admin.site.register(Comment)
