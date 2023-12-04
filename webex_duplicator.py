import sys
import argparse
import json
import requests


class WebexDuplicator:
    src_room_id = ''
    dst_room_id = ''
    src_room_members = []
    dst_room_member_emails = []
    dst_room_members = []

    def __init__(self, src, dst, token):
        self.src_room_name = src
        self.dst_room_name = dst
        self.webex_url = 'https://webexapis.com/v1'
        self.webex_header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        self.get_room_ids()
        self.get_webex_room_members(src_room=True)
        self.get_webex_room_members(src_room=False)
        self.sync_webex_rooms()


    def list_rooms(self, **kwargs):
        query_string = ''
        for k, v in kwargs.items():
            query_string += f'{k}={v}&'
        if len(query_string) > 0:
            query_string = f'?{query_string}'[:-1]
        url = f'{self.webex_url}/rooms{query_string}'
        response = requests.get(url, headers=self.webex_header)
        if 199 < response.status_code < 300:
            rooms = response.json()
            return rooms['items']

    def get_room_ids(self):
        rooms = self.list_rooms(max=1000, type='group')
        for r in rooms:
            if r['title'] == self.src_room_name:
                self.src_room_id = r['id']
                print(f'Found ID for room {self.src_room_name}: {self.src_room_id}')
            if r['title'] == self.dst_room_name:
                self.dst_room_id = r['id']
                print(f'Found ID for room {self.dst_room_name}: {self.dst_room_id}')

    def get_webex_room_members(self, src_room=True):
        if src_room:
            room = self.src_room_id
        else:
            room = self.dst_room_id
        url = f'{self.webex_url}/memberships?roomId={room}'
        response = requests.get(url, headers=self.webex_header)
        if 199 < response.status_code < 300:
            memberships = response.json()
            count = len(memberships['items'])
            if src_room:
                self.src_room_members = memberships['items']
                print(f'Obtained members for room {self.src_room_name}, count:  {count}')
            else:
                self.dst_room_members = memberships['items']
                print(f'Obtained members for room {self.dst_room_name}, count:  {count}')

    def add_webex_room_member(self, room, user, moderator=False):
        url = f'{self.webex_url}/memberships'
        body = {
            'roomId': room,
            'personEmail': user
        }
        print(f'Adding member to room {self.dst_room_name}:  {user}')
        if moderator:
            body.update({'isModerator': True})
        response = requests.post(url, data=json.dumps(body), headers=self.webex_header)
        if 199 < response.status_code < 300:
            return response.json()

    def get_dst_emails(self):
        for s in self.dst_room_members:
            if s['personEmail'] not in self.dst_room_member_emails:
                self.dst_room_member_emails.append(s['personEmail'])

    def sync_webex_rooms(self):
        self.get_dst_emails()
        for m in self.src_room_members:
            if m['personEmail'] not in self.dst_room_member_emails:
                self.add_webex_room_member(self.dst_room_id, m['personEmail'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Webex room membership duplication tool.', prog='Webex Room Duplicator')
    parser.add_argument('--source_room',
                        help='Name of the room you want to duplicate members from',
                        required=True)
    parser.add_argument('--dest_room',
                        help='Name of the room you want to duplicate members to',
                        required=True)
    parser.add_argument('--token', help='Webex authentication bearer token',
                        required=False)
    args = parser.parse_args()
    webex = WebexDuplicator(args.source_room, args.dest_room, args.token)




