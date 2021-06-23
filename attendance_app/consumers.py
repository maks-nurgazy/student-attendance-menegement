import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class AttendanceConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            kind = text_data_json['kind']
            if kind == "reg":
                data = json.dumps({
                    "kind": "reg",
                    "id": text_data_json['id']
                })
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_message',
                        'message': data
                    }
                )
            elif kind == "add":
                data = json.dumps({
                    "kind": "add",
                    "id": text_data_json['id']
                })
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_message',
                        'message': data
                    }
                )
            else:
                data = json.dumps({
                    "kind": "err",
                    "message": "Error occured, contact to Maksatbek"
                })
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_message',
                        'message': data
                    }
                )
        except:
            try:
                id = int(text_data)
                data = json.dumps({
                    "kind": "log",
                    "id": id
                })
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_message',
                        'message': data
                    }
                )
            except ValueError:
                data = json.dumps({
                    "kind": "err",
                    "message": "Invalid data format"
                })
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_message',
                        'message': data
                    }
                )

    def send_message(self, event):
        data = json.dumps(event['message'])
        self.send(text_data=data)
