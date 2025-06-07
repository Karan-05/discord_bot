import discord, os, dotenv, logging
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("READY as", bot.user)

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    print("GOT:", msg.guild, msg.channel, "→", msg.content)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
