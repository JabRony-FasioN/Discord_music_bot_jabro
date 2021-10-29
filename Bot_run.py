import discord
import os
from discord import channel
from discord.ext import commands
#from discord.ext.commands.core import command, guild_only
from discord.flags import Intents
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
from discord import TextChannel
import youtube_dl 
import DiscordUtils

client = commands.Bot(command_prefix='~', Intents = discord.Intents.all())

players = {}

music = DiscordUtils.Music()             

@client.event
async def on_ready():
    print("На месте")

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id = ctx.guild.id)
    if not player:
        player = music.create_player(ctx,ffmpeg_error_betterfix = True)
    if not ctx.voice_client.is_playing():
        await player.queue(url,search = True)
        song = await player.play()
    else:
        song = await player.queue(url,search= True)
    
client.run("ODkzNzg2OTk0MDMzOTYzMDU4.YVgiAQ.qUuPwNCV1zGYB4FcI_L53mnKY3g")
