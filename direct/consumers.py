import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Dialog, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.dialog_id = self.scope['url_route']['kwargs']['dialog_id']
        self.room_group_name = f'chat_{self.dialog_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message', '')

        if not message_text:
            return

        await self.save_message(message_text)

        if message_text.startswith('SHARE_POST:'):
            post_id = message_text.split(':')[1]
            post_data = await self.get_post_data(post_id)

            if post_data:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message_text,
                        'sender': self.scope["user"].username,
                        **post_data
                    }
                )
                return

        # 3. Отправка обычного сообщения
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': self.scope["user"].username,
                'is_share': False
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, text):
        dialog = Dialog.objects.get(id=self.dialog_id)
        return Message.objects.create(
            dialog=dialog,
            sender=self.scope["user"],
            text=text
        )


    @database_sync_to_async
    def get_post_data(self, post_id):
        from posts.models import Post
        try:
            post = Post.objects.get(id=post_id)


            return {
                "is_share": True,
                "post_id": post.id,
                "post_image": post.contentUrl.url if post.contentUrl else "",
                "post_author": post.author.username,
                "post_type": post.post_type,
            }
        except Exception as e:
            print(f"Ошибка получения поста: {e}")
            return None