import asyncio
from twitchio.errors import TwitchIOException
from twitchio.ext import commands

import os

import dotenv

import json
from urllib.request import urlopen

from twitchio.ext.commands.errors import TwitchCommandError

with open("bot/config.json") as config_file:
    config = json.load(config_file)

dotenv.load_dotenv()

import datetime

from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ.get("TOKEN"),
            client_id=os.environ.get("client_id"),
            nick=config["nickname"],
            prefix=config["prefix"],
            initial_channels=config["channels"],
        )

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_ready(self):
        print(f"Twitch Bot Ready | {self.nick}")

    def read_json(self, filename):
        with open(f"{cwd}/{filename}.json", "r") as file:
            data = json.load(file)
        return data

    def write_json(self, data, filename):
        with open(f"{cwd}/{filename}.json", "w") as file:
            json.dump(data, file, indent=4)

    @commands.command(name="ping", aliases=["ding"])
    async def test_command(self, ctx):
        await ctx.send(f"FeelsDankMan 🔔 crossban bot online. @{ctx.author.name}")

    @commands.command(name="cbb_join", aliases=["cbb_joinchannel"])
    async def join_channel(self, ctx, channel: str):
        if ctx.author.name in config["ownernames"]:
            if channel not in config["channels"]:
                data = self.read_json("config")
                data["channels"].append(channel)
                self.write_json(data, "config")

                await self.join_channels([channel])

                print(channel)

                await asyncio.sleep(0.2)

                channel_name = self.get_channel(channel)
                await asyncio.sleep(0.1)
                owner_channel = self.get_channel(config["ownernames"][0])

                await channel_name.send(
                    f"MrDestructoid 🔔 Crossban Bot has joined {channel}!"
                )
                await asyncio.sleep(0.1)
                await owner_channel.send(
                    f"@{config['ownernames'][0]}, Joined {channel}."
                )
            else:
                await ctx.send("Channel already in list.")

        else:
            await ctx.send(
                f"❌ You are not allowed to make Crossban_bot join another channel."
            )

    @commands.command(name="cbb_leave", aliases=["cbb_leavechannel"])
    async def leave_channel(self, ctx, channel: str):
        if ctx.author.name in config["ownernames"] or ctx.author.name == channel:
            if channel in config["channels"]:
                data = self.read_json("config")
                data["channels"].remove(channel)
                self.write_json(data, "config")

                # await self.leave_channels([channel])
                channel_name = self.get_channel(channel)
                await asyncio.sleep(0.1)
                owner_channel = self.get_channel(config["ownernames"][0])

                await channel_name.send(
                    f"MrDestructoid 🔔 Crossban Bot has left {channel} (Will leave once the bot restarts)."
                )
                await asyncio.sleep(0.1)
                await owner_channel.send(f"@{config['ownernames'][0]}, Left {channel}.")
            else:
                await ctx.send(f"❌ Crossban_bot isn't in {channel}")
        else:
            await ctx.send(
                f"❌ You are not allowed to make Crossban_bot leave another channel."
            )

    @commands.command(name="crossban", aliases=["xban"])
    async def crossban_command(self, ctx, user: str, *, reason: str):
        if ctx.author.name in config["ownernames"]:
            for channelname in self.read_json("config")["channels"]:
                await asyncio.sleep(0.2)
                channel = self.get_channel(channelname)
                await channel.send(
                    f".ban {user} Crossbanned, originated from {ctx.channel.name}. Reason: {reason}"
                )

            await ctx.send("Crossban finished :)")

    @commands.command(name="undoban", aliases=["xunban"])
    async def undocrossban_command(self, ctx, user: str):
        if ctx.author.name in config["ownernames"]:
            for channelname in self.read_json("config")["channels"]:
                await asyncio.sleep(0.2)
                channel = self.get_channel(channelname)
                await channel.send(f".unban {user}")

            await ctx.send("Undoban finished :)")

    @commands.command(name="masscrossban", aliases=["massxban", "mxban"])
    async def masscrossban_comamdn(self, ctx, users: str, *, reason: str):
        if ctx.author.name in config["ownernames"]:
            users2 = users.split(",")
            for user in users2:
                for channelname in self.read_json("config")["channels"]:
                    await asyncio.sleep(0.5)
                    channel = self.get_channel(channelname)
                    await channel.send(
                        f".ban {user} Crossbanned, originated from {ctx.channel.name}. Reason: {reason}"
                    )
            await ctx.send("Massban finished :)")

    @commands.command(name="masscrossunban", aliases=["massxunban", "mxuban"])
    async def masscrossunban_comamdn(self, ctx, users: str):
        if ctx.author.name in config["ownernames"]:
            users2 = users.split(",")
            for user in users2:
                for channelname in self.read_json("config")["channels"]:
                    await asyncio.sleep(0.5)
                    channel = self.get_channel(channelname)
                    await channel.send(f".unban {user}")
            await ctx.send("Massunban finished :)")

    @commands.command(name="massfileban")
    async def masscrossban_fromfile(self, ctx, *, url: str):
        if ctx.author.name in config["ownernames"]:
            data = urlopen(url).read().decode("UTF-8")
            users = data.split("\n")
            # print("UserList " + str(users))

            for channelname in self.read_json("config")["channels"]:
                channel = self.get_channel(channelname)
                await asyncio.sleep(0.1)
                await channel.send("Massban starting!")

            for user in users:
                user = user.strip("\r")
                for channelname in self.read_json("config")["channels"]:
                    try:
                        await asyncio.sleep(0.3)
                        channel = self.get_channel(channelname)
                        await channel.send(
                            f".ban {user} | Crossbanned, originated from {ctx.channel.name}."
                        )
                    except:
                        await asyncio.sleep(2)

            for channelname in self.read_json("config")["channels"]:
                channel = self.get_channel(channelname)
                await asyncio.sleep(0.1)
                await channel.send("Massban finished :)")

        else:
            await ctx.send("You are not allowed to do that.")

    @commands.command(name="massfileunban")
    async def masscrossunban_fromfile(self, ctx, *, url: str):
        if ctx.author.name in config["ownernames"]:
            data = urlopen(url).read().decode("UTF-8")
            users = data.split("\n")

            # print("UserList " + str(users))
            for channelname in self.read_json("config")["channels"]:
                await asyncio.sleep(0.1)
                channel = self.get_channel(channelname)
                await channel.send("Massunban starting! (This is usually for false positives)")

            for user in users:
                user = user.strip("\r")
                for channelname in self.read_json("config")["channels"]:
                    try:
                        await asyncio.sleep(0.3)
                        channel = self.get_channel(channelname)
                        await channel.send(f".unban {user}")
                    except:
                        await asyncio.sleep(2)

            for channelname in self.read_json("config")["channels"]:
                await asyncio.sleep(0.1)
                channel = self.get_channel(channelname)
                await channel.send("Massunban finished :)")

        else:
            await ctx.send("You are not allowed to do that.")

    @commands.command(name="sc_massfileban")
    async def massban_fromfile(self, ctx, *, url: str):
        if ctx.author.name in config["ownernames"]:
            data = urlopen(url).read().decode("UTF-8")
            users = data.split("\n")
            # print("UserList " + str(users))

            for user in users:
                user = user.strip("\r")
                try:
                    await asyncio.sleep(0.3)
                    await ctx.channel.send(f".ban {user} | Massbanned")
                except:
                    await asyncio.sleep(2)

            await ctx.send("Massban finished :)")

        else:
            await ctx.send("You are not allowed to do that.")

    @commands.command(name="sc_massfileunban")
    async def massunban_fromfile(self, ctx, *, url: str):
        if ctx.author.name in config["ownernames"]:
            data = urlopen(url).read().decode("UTF-8")
            users = data.split("\n")
            # print("UserList " + str(users))

            for user in users:
                user = user.strip("\r")
                await asyncio.sleep(0.3)
                await ctx.channel.send(f".unban {user}")
                print(user)

            await ctx.send("Massunban finished :)")

        else:
            await ctx.send("You are not allowed to do that.")


bot = Bot()
bot.run()
