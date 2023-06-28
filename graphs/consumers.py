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

class GraphConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print('Websocket Connected....', event)

        self.send({
            'type': 'websocket.accept'
        })
        poll = Poll.objects.get(id='poll-31868258')
        polloptions = poll.options.all()
        user = self.scope['user']

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
        vote = json.loads(event['text'])['message']
        poll = Poll.objects.get(id='poll-31868258')
        print('SIUUU',poll.id)
        totalVotes = poll.total_votes
        polloptionsvotes = poll.options.all()
        polloptions = poll.options.get(choice_name=vote['choice_name'])
        voters = polloptions.voters.all()
        user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(poll.id, self.channel_name)
        print(self.channel_name)
        if vote['status'] == 1:

            if user in voters:
                print('Already Voted Cant Vote')
            elif user not in voters:
                polloptions.choice_votes += 1
                polloptions.voters.add(user)
                polloptions.save()
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

                print(data_dict)

                async_to_sync(self.channel_layer.group_send)(poll.id,
                    {
                    'type': 'websocket.send',
                    'text': data_dict
                    }
                    )
                
                def add_vote(self,event):
                    print('event....',event)
                    # self.send({
                    #     'type': 'websocket.send',
                    #     'text': json.dumps(data_dict)
                    # })
                channel_layer = get_channel_layer()
                channel_layer.router.add_route('add.vote', add_vote)
                print('Voted Successfully')
        elif vote['status'] == 0:
            if user in voters:
                polloptions.choice_votes -= 1
                polloptions.voters.remove(user)
                polloptions.save()
                poll.save()

                print('vote removed')
                print(polloptions.choice_votes)

    def websocket_disconnect(self, event):
        print('Websocket disconnected....')
        poll = Poll.objects.get(id='poll-31868258')
        async_to_sync(self.channel_layer.group_discard)(poll.id, self.channel_name)

        raise StopConsumer()

# class GraphConsumer(AsyncConsumer):

#     async def websocket_connect(self, event):
#         print('Websocket Connected....', event)
#         await self.send({
#             'type': 'websocket.accept'
#         })

#     async def websocket_receive(self, event):
#         print('Websocket recieved message....', event)
#         vote = json.loads(event['text'])['message']

#         poll = await database_sync_to_async(Poll.objects.get)(id=92904581)
#         polloptionsvotes = await database_sync_to_async(poll.options.all)()
#         polloptions = await database_sync_to_async(poll.options.get)(choice_name=vote['choice_name'])
#         voters = await database_sync_to_async(poll.voters.all)()
#         user = self.scope['user']

#         if vote['status'] == 1:

#             if user in voters:
#                 print('Already Voted Cant Vote')
#             elif user not in voters:
#                 polloptions.choice_votes += 1
#                 await database_sync_to_async(polloptions.save)()
#                 await database_sync_to_async(poll.voters.add)(user)
#                 await database_sync_to_async(poll.save)()
#                 print('siuuuuuuuuuuuuuuuuuuuuuu')

#                 data_dict = {}
#                 for index, votes in enumerate(polloptionsvotes):
#                     data_dict[index] = {}
#                     nested_key_name = 'choice_name'
#                     nested_val_name = str(votes.choice_name)
#                     nested_key_votes = 'choice_votes'
#                     nested_val_votes = int(votes.choice_votes)

#                     data_dict[index][nested_key_name] = nested_val_name
#                     data_dict[index][nested_key_votes] = nested_val_votes

#                 print(data_dict)

#                 await self.send({
#                     'type': 'websocket.send',
#                     'text': json.dumps(data_dict),
#                 })

#                 print('Voted Successfully')
#         elif vote['status'] == 0:
#             if user in voters:
#                 polloptions.choice_votes -= 1
#                 await database_sync_to_async(polloptions.save)()
#                 await database_sync_to_async(poll.voters.remove)(user)
#                 await database_sync_to_async(poll.save)()

#                 print('vote removed')
#                 print(polloptions.choice_votes)

#     async def websocket_disconnect(self, event):
#         print('Websocket disconnected....')
#         StopConsumer()
