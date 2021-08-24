import asyncio
from twitchio.ext import commands

import os

import dotenv

import json
from urllib.request import urlopen

with open("config.json") as config_file:
    config = json.load(config_file)

dotenv.load_dotenv()

import datetime

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ.get("TOKEN"),
            client_id=os.environ.get("client_id"),
            nick=config["nickname"],
            prefix=config["prefix"],
            initial_channels=config["channels"],
        )

        self.initial_channels = config["channels"]

    async def event_message(self, message):
        await self.handle_commands(message)

        if config["logmode"]:
            with open(f"logs/log_{datetime.date.today()}.txt", "a") as f:
                f.write("\n" + message.author.name + " - " + message.content + " [" + message.channel.name + "] " + str(datetime.datetime.utcnow()))   

    async def event_ready(self):
        print(f"Twitch Bot Ready | {self.nick}")

    @commands.command(name="ping", aliases=["ding"])    
    async def test_command(self, ctx):
        if config["logmode"]:
            await ctx.send(f"FeelsDankMan 🔔 crossban+log bot online. @{ctx.author.name}")
        else:
            await ctx.send(f"FeelsDankMan 🔔 crossban bot online. @{ctx.author.name}")

    @commands.command(name="crossban", aliases=["xban"])
    async def crossban_command(self, ctx, user: str, *, reason: str):
        if ctx.author.name in config["ownernames"]:
            for channelname in self.initial_channels:
                channel = self.get_channel(channelname)
                await channel.send(f".ban {user} Crossbanned, originated from {ctx.channel.name}. Reason: {reason}")
            
            await ctx.send("Crossban finished :)")

    @commands.command(name="undoban", aliases=["xunban"])
    async def undocrossban_command(self, ctx, user: str):
        if ctx.author.name in config["ownernames"]:
            for channelname in self.initial_channels:
                channel = self.get_channel(channelname)
                await channel.send(f".unban {user}")
            
            await ctx.send("Undoban finished :)")
    
    @commands.command(name="masscrossban", aliases=["massxban", "mxban"])
    async def masscrossban_comamdn(self, ctx, users: str, *, reason: str):
        if ctx.author.name in config["ownernames"]:
            users2 = users.split(",")
            for channelname in self.initial_channels:
                for user in users2:
                    await asyncio.sleep(0.5)
                    channel = self.get_channel(channelname)
                    await channel.send(f".ban {user} Crossbanned, originated from {ctx.channel.name}. Reason: {reason}")
            await ctx.send("Massban finished :)")

    @commands.command(name="masscrossunban", aliases=["massxunban", "mxuban"])
    async def masscrossunban_comamdn(self, ctx, users: str):
        if ctx.author.name in config["ownernames"]:
            users2 = users.split(",")
            for channelname in self.initial_channels:
                for user in users2:
                    await asyncio.sleep(1)
                    channel = self.get_channel(channelname)
                    await channel.send(f".unban {user}")
            await ctx.send("Massunban finished :)")

    @commands.command(name="massfileban")
    async def masscrossban_fromfile(self, ctx, *, url: str):
        if ctx.author.name in config["ownernames"]:
            data = urlopen(url)
            users = data.split("\n")

            for channelname in self.initial_channels:
                for user in users:
                    await asyncio.sleep(2)
                    channel = self.get_channel(channelname)
                    await channel.send(f".ban {user} Crossbanned, originated from {ctx.channel.name}.")

            await ctx.send("Massban finished :)")

        else:
            await ctx.send("You are not allowed to do that.")

    @commands.command(name="massfileunban")
    async def masscrossunban_fromfile(self, ctx, *, url: str):
        if ctx.author.name in config["ownernames"]:
            data = urlopen(url)
            users = data.split("\n")

            for channelname in self.initial_channels:
                for user in users:
                    await asyncio.sleep(2)
                    channel = self.get_channel(channelname)
                    await channel.send(f".unban {user}")

            await ctx.send("Massunban finished :)")

        else:
            await ctx.send("You are not allowed to do that.")

bot = Bot()
bot.run()
