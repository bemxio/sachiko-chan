from discord.ext.commands import Cog
import discord

from io import StringIO
import json
import os

class Admin(Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    @discord.slash_command(description="Get the conversations of the bot.")
    async def conversations(self, ctx: discord.ApplicationContext):
        if not await self.bot.is_owner(ctx.author):
            return await ctx.respond("`You do not have permission to use this command.`")

        cog = self.bot.cogs["Chat"]
        conversations = cog.conversations

        stream = StringIO(json.dumps(conversations, indent=4))
        file = discord.File(stream, filename="conversations.json")

        await ctx.respond(file=file)

    @discord.slash_command(description="Clear all of the conversations of the bot.")
    async def clear(self, ctx: discord.ApplicationContext):
        if not await self.bot.is_owner(ctx.author):
            return await ctx.respond("`You do not have permission to use this command.`")

        # get the "Chat" cog
        cog = self.bot.cogs["Chat"]

        # clear the `conversations` dictionary
        cog.conversations = {}

        # respond to the admin
        await ctx.respond("`Successfully cleared the conversation history.`")

def setup(bot: discord.Bot):
    bot.add_cog(Admin(bot))