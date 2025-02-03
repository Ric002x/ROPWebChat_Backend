import uuid

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from rest_framework.response import Response

from attachments.models import AudioAttachment, FileAttachment
from chats.models import Chat, ChatMessage
from chats.serializers import ChatMessageSerializer
from chats.views.base import BaseView
from setup.socket import socket
from setup.utils.exceptions import ValidationError


class ChatMessagesView(BaseView):
    def get(self, request, chat_id):
        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id
        )

        self.mark_message_as_seen(chat_id, request.user.id)

        socket.emit("mark_message_as_seen", {
            "query": {
                "chat_id": chat_id,
                "exclude_user_id": request.user.id
            }
        })

        messages = ChatMessage.objects.filter(
            chat_id=chat_id, deleted_at__isnull=True,
        ).order_by('created_at').all()

        serializer = ChatMessageSerializer(messages, many=True)

        socket.emit("update_chat", {
            "query": {
                "users": [
                    chat.from_user_id, chat.to_user_id  # type: ignore
                ]
            }
        })

        return Response({
            "messages": serializer.data
        })

    def post(self, request, chat_id):
        body = request.data.get('body')
        file = request.data.get('file')
        audio = request.data.get('audio')

        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id
        )

        self.mark_message_as_seen(chat_id, request.user.id)

        if not body and not file and not audio:
            raise ValidationError("Nenhum parâmetro foi informado")

        attachment = None
        if file:
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / "files",
                settings.MEDIA_URL + "files"
            )

            content_type = file.content_type
            name = file.name.split('.')[0]
            extension = file.name.split('.')[-1]
            size = file.size

            # validate file size:
            if size > 100000000:
                raise ValidationError("O arquivo deve ter no máximo 100MB")

            file = storage.save(f"{uuid.uuid4()}.{extension}", file)
            src = storage.url(file)

            # Saving new attachment
            attachment = FileAttachment.objects.create(
                name=name,
                extension=extension,
                size=size,
                src=src,
                content_type=content_type,
            )
        elif audio:
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / "audios",
                settings.MEDIA_URL + "audios"
            )

            audio = storage.save(f"{uuid.uuid4()}.mp3", audio)
            src = storage.url(audio)

            attachment = AudioAttachment.objects.create(
                src=src
            )

        # Saving Message

        chat_message = ChatMessage.objects.create(
            chat_id=chat_id,
            body=body,
            from_user_id=request.user.id,
            attachment_code="FILE" if file else "AUDIO" if audio else None,
            attachment_id=attachment.pk if attachment else None
        )

        chat_message_data = ChatMessageSerializer(chat_message).data

        socket.emit("update_chat_message", {
            "type": "create",
            "message": chat_message_data,
            "query": {
                "chat_id": chat_id
            }
        })

        # Updating chat viewed_at
        Chat.objects.filter(id=chat_id).update(viewed_at=now())

        socket.emit("update_chat", {
            "query": {
                "users": [
                    chat.from_user_id, chat.to_user_id  # type: ignore
                ]
            }
        })

        return Response({
            "message": chat_message_data
        })


class ChatMessageView(BaseView):
    def delete(self, request, chat_id, message_id):
        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id,
        )

        deleted = ChatMessage.objects.filter(
            id=message_id,
            chat_id=chat_id,
            from_user_id=request.user.id,
            deleted_at__isnull=True
        ).update(
            deleted_at=now()
        )

        if deleted:
            socket.emit("update_chat_message", {
                "type": "delete",
                "query": {
                    "chat_id": chat_id,
                    "message_id": message_id
                }
            })

            socket.emit("update_chat", {
                "query": {
                    "users": [
                        chat.from_user_id, chat.to_user_id  # type: ignore
                    ]
                }
            })

        return Response({
            "success": True
        })
