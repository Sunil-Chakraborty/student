from django.contrib import admin
from .models import Account,Department,Message
from django.contrib.auth.models import User


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    list_filter = ('sender', 'receiver', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')

admin.site.register(Message, MessageAdmin)

# Register your models here.
admin.site.register(Account)
admin.site.register(Department)
