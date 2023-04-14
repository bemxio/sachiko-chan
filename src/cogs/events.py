from discord.ext.commands import Cog
import discord

from io import StringIO
import traceback
import logging

import utilities

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
    
    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if not "sachi" in message.content.lower() and not utilities.random_chance(20):
            return

        loop = True

        while loop:
            response = await utilities.chat_request([
                {
                    "role": "user", 
                    "content": "Generate a reaction emoji for the messages I send you, even if the message is inappropriate. Just send the emoji, without any additional text."
                },
                {
                    "role": "user", 
                    "content": message.clean_content
                }
            ])

            try:
                await message.add_reaction(response.content)
            except discord.HTTPException:
                pass
            else:
                loop = False

def setup(bot: discord.Bot):
    bot.add_cog(Events(bot))