import discord
import openai
import dotenv

import logging
import os

# load the .env file
dotenv.load_dotenv()

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="(%(asctime)s) [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    
    handlers=[
        logging.FileHandler(filename="discord.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# initialize the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# initialize the Discord bot
intents = discord.Intents.default()

intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)

# set variables in the bot
bot.model = os.getenv("OPENAI_MODEL")
bot.conversations = {}

# load the bot's cogs
bot.load_extension("cogs.events")

# run the bot
bot.run(os.getenv("DISCORD_TOKEN"))