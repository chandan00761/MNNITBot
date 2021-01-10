import discord
import json
import re
import os


class MNNITBot(discord.Client):

    def __init__(self, file, intents):
        self.default_role = None
        self.temp_role = None
        self.admin = None
        self.admin_role = None
        self.request_channel = None
        self.test_channel = None
        self.student_file = os.path.join(os.getcwd(), file)
        with open(file) as f:
            self.student_data = json.load(f)
        super().__init__(intents=intents)

    async def on_ready(self):
        self.default_role = self.guilds[0].default_role
        self.temp_role = discord.utils.get(self.guilds[0].roles, name="temp")
        self.admin = self.guilds[0].get_member_named("Hola_Bola_Mdfkr#9935")
        self.admin_role = discord.utils.get(self.guilds[0].roles, name="Administrator")
        self.request_channel = discord.utils.get(self.guilds[0].channels, name="requests")
        self.test_channel = discord.utils.get(self.guilds[0].channels, name="test")
        print(f'{self.user} has connected to Discord')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f"""
                Hi {member.name}, welcome to MNNIT MCA Discord Server!\n
                To access the full server reply your registration number here.\n
                Here is the format <year>CA<roll>
                Eg :- !REG 2020CA001
            """
        )
        await member.add_roles(self.temp_role)

    async def clear_message(self, channel, limit=10):
        msgs = []
        async for message in channel.history(limit=limit):
            msgs.append(message)
        await channel.delete_messages(msgs)

    async def help_message(self, message):
        await message.reply(
            f"""Hi {message.author.name}, welcome to MNNIT MCA Discord Server!
To access the full server reply your registration number here.
Here is the format: 
!REG <year>CA<roll>
Eg :- !REG 2020CA001""")

    def is_me(self, m):
        return m.author == self.user

    async def start_request_poll(self, message):
        request = message.content[8:].strip()
        channel = message.channel
        await channel.purge(limit=1)
        await channel.send(f"""{message.author.name} requested for:
**{request}**

Vote in the below poll.

""")
        await channel.purge(limit=1, check=self.is_me)
        await channel.send(f"""/poll "{request}" """)

    async def registration(self, message):
        user_roll = re.findall("20[0-9]{2}CA[0-9]{3}", message.content)[0]
        if user_roll in self.student_data:
            if not self.student_data[user_roll]["visited"]:
                self.student_data[user_roll]["visited"] = True
                with open(self.student_file, "w") as file:
                    json.dump(self.student_data, file)
                member = self.guilds[0].get_member(message.author.id)
                await member.edit(roles=[self.default_role], nick=self.student_data[user_roll]["name"])
                await member.dm_channel.send(
                    f"""You have successfully registered {message.author.name}. You can now access the full server."""
                )
            else:
                member = self.guilds[0].get_member(message.author.id)
                await member.dm_channel.send(
                    f"""Looks like you have already registered on the server. If you still can't access the server 
then contact the administrator {self.admin.mention} or tell in the WhatsApp group. """
                )
        else:
            await message.reply(f"No such roll exists! {user_roll}. Please check your input.")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if isinstance(message.channel, discord.DMChannel):
            if message.content == "!help":
                await self.help_message(message)
            elif message.content.startswith("!REG"):
                await self.registration(message)

        elif isinstance(message.channel, discord.TextChannel):
            if message.content == "!clear" and self.admin_role in message.author.roles:
                await self.clear_message(message.channel)
            if message.content.startswith("!request") and message.channel.id == self.test_channel.id:
                await self.start_request_poll(message)
