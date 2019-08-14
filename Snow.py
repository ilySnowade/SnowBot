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

@bot.command()
async def ban(ctx, member : discord.Member, *,reason=None):
    await member.ban(reason=reason)
    await ctx.message.delete()

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!:ping_pong: , just joking my ping was {0}'.format(round(bot.latency, 1)))
    class BannedMember(commands.Converter):
    async def convert(self, ctx, arg):
        bans = await ctx.guild.bans()

        try:
            member_id = int(arg)
            user = discord.utils.find(lambda u: u.user.id == member_id, bans)
        except ValueError:
            user = discord.utils.find(lambda u: str(u.user) == arg, bans)

        if user is None:
            return None

        return user


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pg = bot.pg_con

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """ Kick a member from the server """
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f'Member `{member}` kicked.\n'
                       f'Reason: `{reason}`.')

    @commands.command(aliases=['kb'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """ Ban a member from the server """
        await ctx.guild.ban(member, reason=reason, delete_message_days=0)
        await ctx.send(f'Member `{member}` banned.\n'
                       f'Reason: `{reason}`.')

    @commands.command(aliases=['ub'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: BannedMember, *, reason=None):
        """ Unban a member from the server
        Since you can't highlight them anymore use their name#discrim or ID """
        if member is not None:
            await ctx.guild.unban(member.user, reason=reason)
            await ctx.send(f'Member `{member.user}` unbanned.\n'
                           f'Reason: `{reason}`.')

        else:
            await ctx.send("Sorry, I couldn't find that user. Maybe they're not banned :thinking:")

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, num_msg: int):
        """ Remove bot messages from the last X messages """
        if num_msg > 100:
            return await ctx.send('Sorry, number of messages to be deleted must not exceed 100.')

        # Check so that only bot msgs are removed
        def check(message):
            return message.author.id == self.bot.user.id

        try:
            await ctx.channel.purge(check=check, limit=num_msg)
        except Exception as e:
            await ctx.send(f'Failed to delete messages.\n ```py\n{e}```')

    @commands.command(name='prefix', aliases=['set_pre', 'pre'])
    @commands.has_permissions(manage_guild=True)
    async def set_prefix(self, ctx, *, prefix):
        """ Set the server's command prefix for qtbot """
        execute = f'''INSERT INTO custom_prefix (guild_id, prefix) VALUES ({ctx.guild.id}, $1)
                      ON CONFLICT (guild_id) DO 
                          UPDATE SET prefix = $1;'''
        try:
            await self.pg.execute(execute, prefix)
        except Exception as e:
            print(e)
            await ctx.send(f"Sorry, couldn't change prefix to `{prefix}`.")
        else:
            # Update the prefix dict
            self.bot.pre_dict[ctx.guild.id] = prefix

        await ctx.send(f'Changed command prefix to `{prefix}`.')


def setup(bot):
    bot.add_cog(Moderator(bot))
    
 

bot.run(os.getenv('BOT_TOKEN'))

