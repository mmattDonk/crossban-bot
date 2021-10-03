# ❌ Crossban bot

## About
Lets you ban 1 person across multiple chats.

## Features
* Crossbanning across multiple Twitch chats.
* Logging multiple Twitch Chats
* Corssbanning multiple people, across multiple Twitch chats.
* Crossunbanning

## Prerequisites
1. Python
    - Windows: https://www.python.org/downloads/
    - MacOS: https://www.python.org/downloads/
        - MacOS Brew: `brew install python3` & `brew install pip3`

## Setup

1. Edit config_example.json

    1. change config_example.json to `config.json`
    2. Change the contents of it to fit your setup.

2. Fill .env with:
```env
TOKEN=twitchoauthtoken
client_id=twitchdevconsoleclientid
```
**Make sure .env and config.json are in the bot folder**

3. Install requirements `python3 -m pip install -U -r bot/requirements.txt`

4. Start bot `python3 bot/bot.py`

(Or you can skin steps 4 and 5 by using Docker `docker-compose up --build`)

## Commands
### All commands that are bolded, are `OWNER ONLY` (which means only the bot owners can use them)

**!crossban {username} {reason}**

**!undoban {username}**

**!masscrossban {username},{username1},{username2},{username3} {reason}**

**!masscrossunban {username},{username1},{username2},{username3}**


### 🙌 Code Contributors

<table>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a href=https://github.com/mmattbtw>
            <img src=https://avatars.githubusercontent.com/u/30363562?v=4 width="100;"  style="border-radius:50%;align-items:center;justify-content:center;overflow:hidden;padding-top:10px" alt=matt/>
            <br />
            <sub style="font-size:14px"><b>matt</b></sub>
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a href=https://github.com/MrAuro>
            <img src=https://avatars.githubusercontent.com/u/35087590?v=4 width="100;"  style="border-radius:50%;align-items:center;justify-content:center;overflow:hidden;padding-top:10px" alt=Auro/>
            <br />
            <sub style="font-size:14px"><b>Auro</b></sub>
        </a>
    </td>
</tr>
</table>
