from DiscordUtils.Music import Song
import discord
from discord.ext import commands
from discord.ext.commands.core import guild_only
#from discord.ext.commands.core import command, guild_only
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
from discord import TextChannel
import DiscordUtils 
from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio

client = commands.Bot(command_prefix='~', Intents = discord.Intents.all())

players = {}

music = DiscordUtils.Music()             

@client.event
async def on_ready():
    DiscordComponents(client)
    print("На месте")

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

   
@client.command()
async def queue(ctx):
    player = music.get_player(guild_id = ctx.guild.id)
    await ctx.send(f"{','.join([song.name for song in player.current_queue()])}")

@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    msg =await ctx.send(f'Paussed {song.name}')
    await asyncio.sleep(5)
    await msg.delete()
    
@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    msg = await ctx.send(f'Resumed {song.name}')
    await asyncio.sleep(5)
    await msg.delete()

@client.command()
async def loop(ctx):
    player = music.get_player(guild_id =ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        return await ctx.send(f'{song.name} is looping ')
    else:
        return await ctx.send(f'{song.name} is looping ')

@client.command()
async def nowplay(ctx):
    player = music.get_player(guild_id= ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

@client.command()
async def remove(ctx,idx):
    player = music.get_player(guild_id = ctx.guild.id)
    song = await player.remove_from_queue(int(idx))
    msg0 = await ctx.send(f"Removed {song.name} from queue")
    msg = await ctx.send(f'Resumed {song.name}')
    await asyncio.sleep(5)
    await msg.delete()
    await msg0.delete()


@client.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id = ctx.guild.id)
    if not player:
        player = music.create_player(ctx,ffmpeg_error_betterfix = True)
    if not ctx.voice_client.is_playing():
        await player.queue(url,search = True)
        song = await player.play()
        await ctx.send(f'i have started playing {song.name}')
        embed = discord.Embed(title="List of commands.", description="The music", colour=discord.Color.orange())
      #  msg = await ctx.send(embed=embed)
        await ctx.send(content = "option",
        components=[
        Button(style = ButtonStyle.green, label= "resume" ),
        Button(style = ButtonStyle.red, label= "pause" ),
        Button(style = ButtonStyle.blue, label= "remove" )  
    ]) 
        while True:
            response = await client.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.component.label == "resume":
                    await response.edit_origin()
 
                    await resume(ctx)

                elif response.component.label == "pause":
                    await response.edit_origin()

                    await pause(ctx)
                    await response.edit_origin() 

                elif response.component.label == "remove":
                    await remove(ctx, 0)
                    await response.edit_origin()
    else:
        song = await player.queue(url,search= True)
        await ctx.send(f'{song.name} has been added to playlist') 
    
client.run("ODkzNzg2OTk0MDMzOTYzMDU4.YVgiAQ.qUuPwNCV1zGYB4FcI_L53mnKY3g")
