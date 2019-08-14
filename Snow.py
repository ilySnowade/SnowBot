import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.utils import get
import youtube_dl
import os

client = discord.Client
bot = commands.Bot(command_prefix='/')
@bot.event
async def on_ready():
    print('Snow is gonna BLOW')
@bot.command()
async def info(ctx):
    embed = discord.Embed(title="My Info", description="Snow's Info", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="Snow#2307")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="(https://discordapp.com/api/oauth2/authorize?client_id=608204154913161226&permissions=0&scope=bot)")
    await ctx.send(embed=embed)
    
bot.remove_command('help')
    
@bot.command()
 
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of commands:", color=0xeee657)
    embed.add_field(name="/info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="/greet", value="Greet", inline=False)
    embed.add_field(name="/kick", value="Kicks members", inline=False)
    embed.add_field(name="/ban", value="Bans members", inline=False)
    embed.add_field(name="/cat", value="Sends cat gif meow", inline=False)
    embed.add_field(name="/ping", value="Sends bot ping", inline=False)
    
    
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def greet(ctx): 
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")
@bot.command()
async def kick(ctx, member : discord.Member, *,reason=None):
    await member.kick(reason=reason)
    await ctx.message.delete()

@bot.command()
async def ban(ctx, member : discord.Member, *,reason=None):
    await member.ban(reason=reason)
    await ctx.message.delete()

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!:ping_pong: , just joking my ping was {0}'.format(round(bot.latency, 1)))
    @bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

 

bot.run(os.getenv('BOT_TOKEN'))

