import os
import discord
import motor.motor_asyncio

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
mstr = os.getenv("MSTRING")

client = motor.motor_asyncio.AsyncIOMotorClient(mstr)
db = client.rain
greetColl = db["greets"]
linksColl = db["links"]
tagsColl = db["tags"]

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

for files in os.listdir("./cogs"):
    if files.endswith(".py"):
        cogf = files[:-3]
        try:
            bot.load_extension(f"cogs.{cogf}")
            print(f"{cogf} initialized!")
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    print("we have logged in")

bot.run(token)