import discord
import json
import re
import os


class MNNITBot(discord.Client):

    def __init__(self, file, intents):
        self.default_role = None
        self.temp_role = None
        self.admin_role = None
        self.student_file = os.path.join(os.getcwd(), file)
        with open(file) as f:
            self.student_data = json.load(f)
        super().__init__(intents=intents)

    async def on_ready(self):
        self.default_role = self.guilds[0].default_role
        self.temp_role = discord.utils.get(self.guilds[0].roles, name="temp")
        self.admin_role = discord.utils.get(self.guilds[0].roles, name="Administrator")
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

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if isinstance(message.channel, discord.DMChannel):
            if message.content == "!help":
                await message.reply(f"""
                            Hi {message.author.name}, welcome to MNNIT MCA Discord Server!
            To access the full server reply your registration number here.
            Here is the format: 
                !REG <year>CA<roll>
            Eg :- !REG 2020CA001
                        """)
            elif message.content.startswith("!REG"):
                user_roll = re.findall("20[0-9]{2}CA[0-9]{3}", message.content)[0]
                if user_roll in self.student_data:
                    if not self.student_data[user_roll]["visited"]:
                        self.student_data[user_roll]["visited"] = True
                        with open(self.student_file, "w") as file:
                            json.dump(self.student_data, file)
                        member = self.guilds[0].get_member(message.author.id)
                        await member.edit(roles=[self.default_role], nick=self.student_data[user_roll]["name"])

                else:
                    await message.reply(f"No such roll exists! {user_roll}")
        elif isinstance(message.channel, discord.TextChannel):
            if message.content == "!clear" and self.admin_role in message.author.roles:
                await self.clear_message(message.channel)
