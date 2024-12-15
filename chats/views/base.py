from django.db.models import Q
from django.utils.timezone import now
from rest_framework.views import APIView

from chats.models import Chat, ChatMessage
from chats.serializers import ChatSerializer
from chats.utils.exceptions import ChatNotFound, UserNotFound
from users.models import User


class BaseView(APIView):
    def get_user(self, raise_exception=True, **kwargs) -> User | None:
        user = User.objects.filter(**kwargs).first()

        if not user and raise_exception:
            raise UserNotFound

        return user

    def has_existing_chat(self, user_id, to_user) -> Chat | None:
        chat = Chat.objects.filter(
            Q(from_user=user_id) & Q(to_user=to_user),
            Q(to_user=to_user) & Q(from_user=user_id)
        ).first()

        serializer = ChatSerializer(chat, context={'user_id': user_id}).data

        if not chat:
            return None

        return serializer  # type: ignore

    def chat_belongs_to_user(self, chat_id, user_id) -> Chat | None:
        chat = Chat.objects.filter(
            Q(from_user=user_id) | Q(to_user_id=user_id),
            id=chat_id,
            deleted_at__isnull=True
        ).first()

        if not chat:
            raise ChatNotFound

        return chat

    def mark_message_as_seen(self, chat_id, user_id) -> None:
        ChatMessage.objects.filter(
            chat_id=chat_id,
            viewed_at__isnull=True,
            deleted_at__isnull=True
        ).exclude(from_user=user_id).\
            update(viewed_at=now())
