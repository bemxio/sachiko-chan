from discord.ext.commands import Cog
import discord

from io import StringIO
import traceback
import logging

class Events(Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        logging.info(f"Logged in as {self.bot.user}!")

    @Cog.listener()
    async def on_command_error(self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError):
        exception = traceback.format_exception(type(error), error, error.__traceback__)

        message = (
            "Uh oh, I've ran into an issue while trying to execute this command!\n"
            "Please send the file below to the bot developers via DMs:\n"
        )
        
        stream = StringIO("".join(exception))
        file = discord.File(stream, filename="error.log")

        logging.warning(f"A user tried to use `/{ctx.command}` but got an error: {error}")

        await ctx.respond(message, file=file)

def setup(bot: discord.Bot):
    bot.add_cog(Events(bot))