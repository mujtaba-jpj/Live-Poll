# chat/consumers.py
import json
from time import sleep
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.generic.websocket import WebsocketConsumer
import asyncio
import json
from .models import Poll, PollChoices
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer


class PollConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print('Websocket Connected....', event)

        self.send({
            'type': 'websocket.accept'
        })



        poll_id = self.scope['url_route']['kwargs'].get('id')
        poll = Poll.objects.get(id=poll_id)
        polloptions = poll.options.all()
        user = self.scope['user']

        async_to_sync(self.channel_layer.group_add)(poll.id, self.channel_name)

        try:
            voter = polloptions.get(voters=user)
            data_dict = {}
            data_dict['voted_user_option'] = voter.choice_name
            print(data_dict)
            self.send({
                'type': 'websocket.send',
                'text': json.dumps(data_dict)
            })
        except ObjectDoesNotExist:
            pass

    def websocket_receive(self, event):
        print('Websocket recieved message....', event)


        poll_id = self.scope['url_route']['kwargs'].get('id')
        vote = json.loads(event['text'])['message']
        poll = Poll.objects.get(id=poll_id)
        totalVotes = poll.total_votes
        polloptionsvotes = poll.options.all()
        selectedOption = poll.options.get(choice_name=vote['choice_name'])
        voters = selectedOption.voters.all()
        user = self.scope['user']


        if vote['status'] == 1:

            if user in voters:
                print('Already Voted Cant Vote')

            elif user not in voters:
                selectedOption.choice_votes += 1
                selectedOption.voters.add(user)
                selectedOption.save()
                poll.save()
                totalVotes = poll.total_votes

                data_dict = {}
                for index, votes in enumerate(polloptionsvotes):

                    data_dict[index] = {}
                    nested_key_name = 'choice_name'
                    nested_val_name = str(votes.choice_name)
                    nested_key_votes = 'choice_votes'
                    nested_val_votes = int(votes.choice_votes)

                    data_dict[index][nested_key_name] = nested_val_name
                    data_dict[index][nested_key_votes] = nested_val_votes
                    if index == len(polloptionsvotes) - 1:
                        i = index + 1
                        data_dict[i] = {}
                        print(i)
                        data_dict[i]['total_votes'] = totalVotes

                # print(type(json.dumps(data_dict)))

                # self.send({
                #     'type': 'websocket.send',
                #     'text': json.dumps(data_dict)
                # })
                async_to_sync(self.channel_layer.group_send)(
                    poll.id, {"type": "add_vote",
                              "text": json.dumps(data_dict)}
                )

        elif vote['status'] == 0:
            if user in voters:
                selectedOption.choice_votes -= 1
                selectedOption.voters.remove(user)
                selectedOption.save()
                poll.save()

                print('vote removed')
                print(selectedOption.choice_votes)

    def add_vote(self, event):
        message = event['text']

        self.send({
            'type': 'websocket.send',
            'text': message
        })

    def websocket_disconnect(self, event):
        print('Websocket disconnected....')
        poll = Poll.objects.get(id='poll-31868258')
        async_to_sync(self.channel_layer.group_discard)(
            poll.id, self.channel_name)

        raise StopConsumer()


# class GraphConsumer(WebsocketConsumer):

#     def connect(self):
#         print('Websocket Connected....')

#         self.poll = Poll.objects.get(id='poll-31868258')
#         self.polloptions = self.poll.options.all()
#         self.user = self.scope['user']

#         async_to_sync(self.channel_layer.group_add)(
#             self.poll.id, self.channel_name)
#         self.accept()

#         try:
#             voter = self.polloptions.get(voters=self.user)
#             data_dict = {}
#             data_dict['voted_user_option'] = voter.choice_name
#             print(data_dict)
#             self.send(text_data=json.dumps(data_dict))

#         except ObjectDoesNotExist:
#             pass

#     def receive(self, text_data):
#         print('Websocket recieved message....', text_data)

#         vote = json.loads(text_data)['message']

#         polloptions = self.poll.options.get(choice_name=vote['choice_name'])
#         voters = polloptions.voters.all()
#         print(self.channel_name)
#         if vote['status'] == 1:

#             if self.user in voters:
#                 print('Already Voted Cant Vote')

#             elif self.user not in voters:
#                 polloptions.choice_votes += 1
#                 polloptions.voters.add(self.user)
#                 polloptions.save()
#                 self.poll.save()

#                 async_to_sync(self.channel_layer.group_send)(
#                     self.poll.id, {"type": "add_vote",
#                                    "message": vote['choice_name']}
#                 )

#                 print('Voted Successfully')

#         elif vote['status'] == 0:
#             if self.user in voters:
#                 polloptions.choice_votes -= 1
#                 polloptions.voters.remove(self.user)
#                 polloptions.save()
#                 self.poll.save()

#                 print('vote removed')
#                 print(polloptions.choice_votes)

#     def add_vote(self, event):
#         message = event["message"]
#         totalVotes = self.poll.total_votes

#         data_dict = {}
#         for index, votes in enumerate(self.polloptions):

#             data_dict[index] = {}
#             nested_key_name = 'choice_name'
#             nested_val_name = str(votes.choice_name)
#             nested_key_votes = 'choice_votes'
#             nested_val_votes = int(votes.choice_votes)

#             data_dict[index][nested_key_name] = nested_val_name
#             data_dict[index][nested_key_votes] = nested_val_votes
#             if index == len(self.polloptions) - 1:
#                 i = index + 1
#                 data_dict[i] = {}
#                 print(i)
#                 data_dict[i]['total_votes'] = totalVotes

#         self.send(text_data=json.dumps(data_dict))

#         print('Dictionary...', data_dict)

#     def disconnect(self, close_code):
#         print('Websocket disconnected....')
#         poll = Poll.objects.get(id='poll-31868258')
#         async_to_sync(self.channel_layer.group_discard)(
#             poll.id, self.channel_name
#         )
#         raise StopConsumer()
