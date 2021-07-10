from twitchio.ext import commands

import os

import dotenv

import json

with open("config.json") as config_file:
    config = json.load(config_file)

dotenv.load_dotenv()

import datetime

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=os.environ.get("TOKEN"),
            client_id=os.environ.get("client_id"),
            nick=config["nickname"],
            prefix=config["prefix"],
            initial_channels=config["channels"],
        )

    async def event_message(self, message):
        await self.handle_commands(message)
        print(
            f"[MESSAGE LOGS] ({message.channel.name}) "
            + message.author.name
            + " - "
            + message.content
        )
        if config["logmode"]:
            f = open(f"logs/log_{datetime.date.today()}.txt", "a")
            f.write("\n" + message.author.name + " - " + message.content + " [" + message.channel.name + "] " + str(datetime.datetime.utcnow()))
            f.close()   

    async def event_ready(self):
        print(f"Twitch Bot Ready | {self.nick}")

    @commands.command(name="ping", aliases=["ding"])    
    async def test_command(self, ctx):
        await ctx.send(f"FeelsDankMan 🔔 ding @{ctx.author.name}")

    @commands.command(name="crossban", aliases=["xban"])
    async def crossban_command(self, ctx, user: str, *, reason: str):
        if ctx.author.name in config["ownernames"]:
            for channelname in self.initial_channels:
                channel = self.get_channel(channelname)
                await channel.ban(user, reason=f"Crossbanned, originated from {ctx.channel.name}. Reason: {reason}")
            
            await ctx.send("Crossban finished :)")

    @commands.command(name="undoban", aliases=["xunban"])
    async def undocrossban_command(self, ctx, user: str):
        if ctx.author.name in config["ownernames"]:
            for channelname in self.initial_channels:
                channel = self.get_channel(channelname)
                await channel.unban(user)
            
            await ctx.send("Undoban finished :)")

bot = Bot()
bot.run()