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
    embed.add_field(name="/help", value="Gives helps command", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def greet(ctx): 
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")
  @bot.command(pass_context = True)
async def mute(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '194151340090327041':
        role = discord.utils.get(member.server.roles, name='Muted')
        await bot.add_roles(member, role)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await bot.say(embed=embed)

    
bot.run(os.getenv('BOT_TOKEN'))

