from django.contrib import admin

from chats.models import Chat, ChatMessage

# Register your models here.


@admin.register(Chat)
class AudioAttachmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user']


@admin.register(ChatMessage)
class FileAttachmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'body', 'attachment_id', 'created_at']
