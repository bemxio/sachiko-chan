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

intents.messages = True
intents.members = True

bot = discord.Bot(intents=intents)

# set variables in the bot
bot.conversations = {}

with open("src/prompt.txt", "r", encoding="utf-8") as file:
    bot.initial_prompt = file.read()

# load the bot's cogs
bot.load_extension("cogs.events")
bot.load_extension("cogs.chat")

# run the bot
bot.run(os.getenv("DISCORD_TOKEN"))