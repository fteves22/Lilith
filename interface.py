import discord
import discord
from discord.ext import commands
import discord.ext
import re

from initTracker import *

TOKEN = ""
client = discord.Client()

description = '''Lilith is a Discord bot designed to make Dungeons & Dragons easier to play and manage.'''
bot = commands.Bot(command_prefix='!', description=description)

# ----------------------------------------------------------------------------------------------------
#                                      GENERAL BOT FUNCTIONS
# ----------------------------------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def clean(ctx):    
    def is_bot(m):
        return m.author == bot.user

    def is_command(m):
        return m.content[0] == bot.command_prefix

    await ctx.channel.purge(check = is_command)
    await ctx.channel.purge(check = is_bot)

# ----------------------------------------------------------------------------------------------------
#                                       INITIATIVE TRACKING
# ----------------------------------------------------------------------------------------------------

# Create the Initiative Tracker object.
tracker = InitTracker()

@bot.command()
async def join(ctx, *arg):
    ''' Adds a combatant as [name] to the combat order with i for their initiative roll.
        !join [name] [i] '''

    if len(arg) < 2:
        await ctx.send("To join initiative, the input must be in the form: `[name] [initiative roll]`.")
    else:
        username = ctx.message.author
        name = " ".join(arg[:-1])
        initRoll = arg[-1]

        msg = tracker.join(username, name, initRoll)
        await ctx.send(username.mention + " " + msg)

@bot.command()
async def kill(ctx, *arg):
    ''' Deletes the combatant [name] if they exist in the combat order.
        !delete [name] '''

    username = ctx.message.author
    name = " ".join(arg)

    msg = tracker.kill(name)
    await ctx.send(username.mention + " " + msg)

@bot.command()
async def begin(ctx):
    ''' Begins combat, and tags the first player in combat.
        !begin '''

    result = tracker.begin()
    botMessage = await ctx.send(result)
    tracker.last_message = botMessage.id

    if tracker.rounds != 0:
        await botMessage.add_reaction("⏮️")
        await botMessage.add_reaction("⏭️")

@bot.command()
async def end(ctx):
    ''' Ends combat, and clears the tracker of all player information.
        !end '''

    result = tracker.end()
    await ctx.send(result)

@bot.command()
async def next(ctx):
    ''' Moves onto the next player in combat.
        !next '''

    result = tracker.next()
    botMessage = await ctx.send(result)
    tracker.last_message = botMessage.id

    if tracker.rounds != 0:
        await botMessage.add_reaction("⏮️")
        await botMessage.add_reaction("⏭️")

@bot.command()
async def prev(ctx):
    ''' Moves back to the previous player in combat.
        !prev '''
    result = tracker.prev()
    botMessage = await ctx.send(result)
    tracker.last_message = botMessage.id

    if tracker.rounds != 0:
        await botMessage.add_reaction("⏮️")
        await botMessage.add_reaction("⏭️")

@bot.command()
async def previous(ctx):
    ''' Moves back to the previous player in combat.
        !previous '''
    await prev(ctx)

@bot.command()
async def show(ctx):
    ''' Allows you to view the current combat order.
        !show '''

    result = tracker.printTracker()
    botMessage = await ctx.send(result)
    tracker.last_message = botMessage.id

    if tracker.rounds != 0:
        await botMessage.add_reaction("⏮️")
        await botMessage.add_reaction("⏭️")

@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    message = reaction.message
    message_id = message.id
    channel = message.channel

    current = tracker.trackerInfo[tracker.currentPlayer][0]

    if user == current and tracker.last_message == message_id:
        if emoji == "⏮️":
            await prev(channel)
        elif emoji == "⏭️":
            await next(channel)
        else:
            return


bot.run(TOKEN)
