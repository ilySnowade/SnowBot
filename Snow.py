import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
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
@commands.has_permissions(administrator=True)
async def kick(ctx, member:discord.Member = None):
    if not member:
        await ctx.send("Please specify a member")
        return
    await member.kick()
    await ctx.send(f"{member.mention} got kicked")
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to kick people")

@bot.command()
async def ban(ctx, member : discord.Member, *,reason=None):
    await member.ban(reason=reason)
    await ctx.message.delete()
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!:ping_pong: , just joking my ping was {0}'.format(round(bot.latency, 1)))
 

    
bot.run(os.getenv('BOT_TOKEN'))

