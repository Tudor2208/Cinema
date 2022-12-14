from django.contrib import admin
# Register your models here.

from .models import Message
 
@admin.register(Message)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in Message._meta.get_fields()]