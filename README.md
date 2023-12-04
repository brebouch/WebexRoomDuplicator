# Webex Room Duplicator

This tool is used to duplicate Webex room members from one room to another.

## Installation

1. Clone the repository
2. Install dependencies with `pip install -r requirements.txt`


## Usage

#### Requires the following flags

* --source_room -- The name of the room to copy members from
* --dest_room -- The name of the room to copy member to
* --token -- The Webex bearer token for authenticating API calls

Runs from command line `python3 webex_duplicator --source_room $SOURCE_ROOM --dest_room $DEST_ROOM --token $TOKEN`

## Considerations

The owner of the token, whether person or bot, must be a member of both rooms and moderator of destination room for app to work.