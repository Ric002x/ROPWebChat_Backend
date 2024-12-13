from django.contrib import admin

from attachments.models import AudioAttachment, FileAttachment

# Register your models here.


@admin.register(AudioAttachment)
class AudioAttachmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'src']


@admin.register(FileAttachment)
class FileAttachmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'extension']
    list_editable = ['name']
