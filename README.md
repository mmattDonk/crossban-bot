# ❌ Crossban bot

## About
Lets you ban 1 person across multiple chats.

## Features
* Crossbanning across multiple Twitch chats.
* Logging multiple Twitch Chats
* Corssbanning multiple people, across multiple Twitch chats.
* Crossunbanning


## Setup

1. Edit config_example.json

    1. change config_example.json to `config.json`
    2. Change the contents of it to fit your setup.

2. Fill .env with:
```env
TOKEN=twitchoauthtoken
client_id=twitchdevconsoleclientid
```

3. Make a "logs" folder (if you have logging enabled)

4. Install requirements `python3 -m pip install -U -r requirements.txt`

5. Start bot `python3 bot.py`

## commands
!crossban username reason

!undoban username

!masscrossban username,username1,username2,username3 reason

!masscrossunban username,username1,username2,username3
