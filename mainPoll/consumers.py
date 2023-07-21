# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.consumer import SyncConsumer
import json
from .models import Poll
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


class PollConsumer(SyncConsumer):

    def websocket_connect(self, event):

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
        print('STAGE 1 PASSED')

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
                        data_dict[i]['total_votes'] = totalVotes

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

    def add_vote(self, event):
        message = event['text']

        self.send({
            'type': 'websocket.send',
            'text': message
        })

    def websocket_disconnect(self, event):
        poll_id = self.scope['url_route']['kwargs'].get('id')
        poll = Poll.objects.get(id=poll_id)
        async_to_sync(self.channel_layer.group_discard)(
            poll.id, self.channel_name)

        raise StopConsumer()
