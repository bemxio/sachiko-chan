from discord.ext.commands import Cog
import discord

import utilities

class Chat(Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot
        self.conversations: dict = {}

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        # ignore messages sent by the bot
        if message.author == self.bot.user:
            return

        # ignore messages that aren't mentioning the bot
        if not utilities.is_mentioned(self.bot.user, message):
            return

        author = str(message.author.id)

        content = message.clean_content.replace(f"@{self.bot.user.name}", "")
        content = content.strip()

        if author not in self.conversations:
            self.conversations[author] = [{"role": "user", "content": self.bot.initial_prompt}]

        self.conversations[author].append({
            "role": "user", "content": content
        })

        with message.channel.typing():
            response = await utilities.chat_request(self.conversations[author])

        content = utilities.filter_markdown(response.content)

        # append the bot's response to the conversation
        self.conversations[author].append(response)

        # send the bot's response
        await message.reply(content, mention_author=False)

    @discord.slash_command(description="Makes Sachiko-chan forget the message history with you.")
    async def forget(self, ctx: discord.ApplicationContext):
        author = str(ctx.author.id)

        if author in self.conversations:
            self.conversations[author] = [{"role": "user", "content": self.bot.initial_prompt}]

        await ctx.respond("`Successfully cleared your conversation history.`")

def setup(bot: discord.Bot):
    bot.add_cog(Chat(bot))