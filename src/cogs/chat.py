from discord.ext.commands import Cog
import discord
import openai

import functools
import os

def filter_markdown(text: str) -> str:
    filtered = text.replace("\\", "\\\\") # escape backslashes first

    filtered = filtered.replace("*", "\\*")
    filtered = filtered.replace("_", "\\_")
    filtered = filtered.replace("~", "\\~")

    filtered = filtered.replace("`", "\\`")

    filtered = filtered.replace(">", "\\>")
    filtered = filtered.replace("|", "\\|")

    return filtered

class Chat(Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot
        self.conversations: dict = {}

    def is_mentioned(self, message: discord.Message) -> bool:
        if isinstance(message.channel, discord.DMChannel):
            return True

        if self.bot.user.mentioned_in(message):
            return True

        return False

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        # ignore messages sent by the bot
        if message.author == self.bot.user:
            return

        # ignore messages that aren't mentioning the bot
        if not self.is_mentioned(message):
            return

        author = str(message.author.id)

        content = message.clean_content.replace(f"@{self.bot.user.name}", "")
        content = content.strip()

        if author not in self.conversations:
            self.conversations[author] = [{"role": "user", "content": self.bot.initial_prompt}]

        self.conversations[author].append({
            "role": "user", "content": content
        })

        # trigger typing indicator while ChatCompletion is running
        await message.channel.trigger_typing()

        function = functools.partial(
            openai.ChatCompletion.create, 

            model=os.getenv("OPENAI_MODEL"), 
            messages=self.conversations[author]
        )
        response = await self.bot.loop.run_in_executor(None, function)

        response = response.choices[0].message
        content = response.content

        # append the bot's response to the conversation
        self.conversations[author].append(dict(response))

        # send the bot's response
        await message.reply(filter_markdown(content), mention_author=False)

    @discord.slash_command(description="Makes Sachiko-chan forget the message history with you.")
    async def forget(self, ctx: discord.ApplicationContext):
        author = str(ctx.author.id)

        if author in self.conversations:
            self.conversations[author] = [{"role": "user", "content": self.bot.initial_prompt}]

        await ctx.respond("`Successfully cleared your conversation history.`")

def setup(bot: discord.Bot):
    bot.add_cog(Chat(bot))