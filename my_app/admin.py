from django.contrib import admin

from my_app import models

# Register your models here.
admin.site.register(models.Interest)
admin.site.register(models.ChatMessage)
