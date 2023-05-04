# Sachiko-chan
A Discord chat bot, being an overexcited anime girl that loves ice cream, using a lot of "[UwU speech](https://www.urbandictionary.com/define.php?term=UwU%20Speech)" and [kaomojis](https://en.wikipedia.org/wiki/Emoticon#Japanese_(kaomoji)).

Made using [OpenAI's API](https://platform.openai.com/docs/api-reference/chat) and [Pycord](https://pycord.dev), for ~~the lack of affection in my life~~ fun and silliness!

## Running
To run the bot, make sure you have Python 3.8 or higher installed. You can download it [here](https://www.python.org/downloads/).

You will need to create a Discord application in the [Discord Developer Portal](https://discord.com/developers/applications), and add a bot to it. You can find a guide on how to do that [here](https://discordpy.readthedocs.io/en/stable/discord.html).
You will also need an OpenAI API key, which you can get by creating an account [here](https://beta.openai.com/).

1. Clone the repository, either by downloading the ZIP file on GitHub, or by using `git clone`.
2. Move to the directory in your terminal.
3. Install the dependencies using `pip install -r requirements.txt`.
4. Create a file called `.env` in the root directory of the project, and add the following:

    ```
    DISCORD_TOKEN=<your token here>
    OPENAI_API_KEY=<your key here>
    ```

    where `<your token here>` is your Discord bot token, and `<your key here>` is your OpenAI API key.

5. Run the bot using `python main.py`.

## Contributing
Whether you have an issue or if you want to add a feature, feel free to open an issue or a pull request. I'll be happy to look at it, and potentially merge it!