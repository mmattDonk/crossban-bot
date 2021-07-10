## crossban bot

edit config_example.json

change config_example.json to `config.json`

fill .env with:
```env
TOKEN=twitchoauthtoken
client_id=twitchdevconsoleclientid
```

make a "logs" folder (if you have logging enabled)

install requirements `python3 -m pip install -U -r requirements.txt`

start bot `python3 bot.py`

## commands
!crossban username reason

!undoban username

!masscrossban username,username1,username2,username3 reason

!masscrossunban username,username1,username2,username3