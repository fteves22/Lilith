import discord
import discord
from discord.ext import commands
import discord.ext
import re

from initTracker import *
from prefixes import *

TOKEN = "NzgyNjk3MDY1NjE2NjM3OTcy.X8P9cg.PQXJoSU_0jedi8xoxsF2zcyc0AQ"
client = discord.Client()

description = '''Lilith is a Discord bot designed to make Dungeons & Dragons easier to play and manage.'''

# ----------------------------------------------------------------------------------------------------
#                                              PREFIX
# ----------------------------------------------------------------------------------------------------

p = Prefixes()

def _prefix_callable(bot, msg):
    guild = msg.guild.id
    if p.prefixInfo == []:
        return "!"
    else:
        return p.getPrefix(guild)

bot = commands.Bot(command_prefix=_prefix_callable, description=description)

@bot.command()
async def setPrefix(ctx, arg):
    guild = ctx.message.guild.id
    prefix = arg

    if prefix == '':
        return "Prefix required."

    await ctx.send("Prefix: `" + p.setPrefix(guild, prefix) + "`")

@bot.command()
async def prefix(ctx):
    guild = ctx.message.guild.id
    await ctx.send("Prefix: `" + _prefix_callable(bot, ctx.message) + "`")

@bot.command()
async def showAll(ctx):
    p.showPrefixes()

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

    await ctx.channel.purge(limit = 1)
    await ctx.channel.purge(check = is_bot)

@bot.command()
async def purgeAll(ctx, amount = 10):
    await ctx.channel.purge(limit=amount)

# ----------------------------------------------------------------------------------------------------
#                                       INITIATIVE TRACKING
# ----------------------------------------------------------------------------------------------------

allTrackers = []

@bot.command()
async def join(ctx, *arg):
    ''' Adds a combatant as [name] to the combat order with i for their initiative roll.
        !join [name] [i] '''
    
    # Delete command message.
    await ctx.message.delete()

    # Missing parameters.
    if len(arg) < 2:
        await ctx.send("To join initiative, the input must be in the form: `[name] [initiative roll]`.")
    else:
        username = ctx.message.author
        name = " ".join(arg[:-1])
        initRoll = arg[-1]

        # Determine tracker.
        found = False
        for data in allTrackers:
            if data[0] == ctx.message.guild.id:
                tracker = data[1]
                found = True
                break
        
        if not found:
            tracker = InitTracker()
            allTrackers.append([ctx.message.guild.id, tracker])

        msg = tracker.join(username, name, initRoll)
        await ctx.send(username.mention + " " + msg)

@bot.command()
async def kill(ctx, *arg):
    ''' Deletes the combatant [name] if they exist in the combat order.
        !delete [name] '''

    # Delete command message.
    await ctx.message.delete()

    username = ctx.message.author
    name = " ".join(arg)

    # Determine tracker.
    found = False
    for data in allTrackers:
        if data[0] == ctx.message.guild.id:
            tracker = data[1]
            found = True
            break
    
    if not found:
        await ctx.send("Initiative tracker hasn't been instantiated.\nUse `!join [name] [i]` to add a combatant to initiative.")

    msg = tracker.kill(name)
    await ctx.send(username.mention + " " + msg)

@bot.command()
async def begin(ctx):
    ''' Begins combat, and tags the first player in combat.
        !begin '''
    
    # Delete command message.
    await ctx.message.delete()
    
    # Determine tracker.
    found = False
    for data in allTrackers:
        if data[0] == ctx.message.guild.id:
            tracker = data[1]
            found = True
            break
    
    if not found:
        await ctx.send("Initiative tracker hasn't been instantiated.\nUse `!join [name] [i]` to add a combatant to initiative.")

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
    
    # Delete command message.
    await ctx.message.delete()
    
    # Determine tracker.
    found = False
    for data in allTrackers:
        if data[0] == ctx.message.guild.id:
            tracker = data[1]
            found = True
            break
    
    if not found:
        await ctx.send("Initiative tracker hasn't been instantiated.\nUse `!join [name] [i]` to add a combatant to initiative.")

    result = tracker.end()
    await ctx.send(result)

@bot.command()
async def next(ctx):
    ''' Moves onto the next player in combat.
        !next '''
    
    # Delete command message.
    try:
        await ctx.message.delete()
    except Exception:
        pass
    
    # Determine tracker.
    found = False
    for data in allTrackers:
        if data[0] == ctx.guild.id:
            tracker = data[1]
            found = True
            break
    
    if not found:
        await ctx.send("Initiative tracker hasn't been instantiated.\nUse `!join [name] [i]` to add a combatant to initiative.")

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
    
    # Delete command message.
    try:
        await ctx.message.delete()
    except Exception:
        pass
    
    # Determine tracker.
    found = False
    for data in allTrackers:
        if data[0] == ctx.guild.id:
            tracker = data[1]
            found = True
            break
    
    if not found:
        await ctx.send("Initiative tracker hasn't been instantiated.\nUse `!join [name] [i]` to add a combatant to initiative.")
        
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
    
    # Delete command message.
    await ctx.message.delete()
    
    # Determine tracker.
    found = False
    for data in allTrackers:
        if data[0] == ctx.message.guild.id:
            tracker = data[1]
            found = True
            break
    
    if not found:
        await ctx.send("Initiative tracker hasn't been instantiated.\nUse `!join [name] [i]` to add a combatant to initiative.")
        return

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
        
    # Determine tracker.
    found = False
    for data in allTrackers:
        if data[0] == message.guild.id:
            tracker = data[1]
            found = True
            break
    
    if not found:
        await channel.send("Initiative tracker hasn't been instantiated.\nUse `!join [name] [i]` to add a combatant to initiative.")

    current = tracker.trackerInfo[tracker.currentPlayer][0]

    if user == current and tracker.last_message == message_id:
        if emoji == "⏮️":
            await prev(channel)
        elif emoji == "⏭️":
            await next(channel)
        else:
            return


bot.run(TOKEN)
