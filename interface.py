import discord
import discord
from discord.ext import commands
import discord.ext
import re
import os

from initTracker import *
from prefixes import *
import diceRoll

TOKEN = os.environ["TOKEN"]
client = discord.Client()

description = '''Lilith is a Discord bot designed to make Dungeons & Dragons easier to play and manage.'''

# ----------------------------------------------------------------------------------------------------
#                                              PREFIX
# ----------------------------------------------------------------------------------------------------

# Create prefix object.
p = Prefixes()

def _prefix_callable(bot, msg):
    prefix = '!'
    guild = msg.guild
    if p.prefixInfo == []:
        pass
    else:
        prefix = p.getPrefix(guild)
    
    return prefix

bot = commands.Bot(command_prefix=_prefix_callable, description=description, help_command = None)

@bot.command()
async def setPrefix(ctx, arg = ''):
    guild = ctx.message.guild
    prefix = arg

    # Delete command message.
    await ctx.message.delete()

    if arg == '':
        await ctx.send("⚠️ Prefix required. Use `setPrefix [p]` to set your server's prefix.")
    else:
        await ctx.send("Prefix: `" + p.setPrefix(guild, prefix) + "`")

@bot.command()
async def showAllPrefixes(ctx):
    # Delete command message.
    await ctx.message.delete()
    
    p.showPrefixes()

# ----------------------------------------------------------------------------------------------------
#                                      GENERAL BOT FUNCTIONS
# ----------------------------------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game("D&D 5E | !help"))

@bot.command()
async def help(ctx, arg = ''):
    p = _prefix_callable(bot, ctx.message)

    helpMsg = "`help`: Shows a list of common commands, and a link to a list of all commands."
    setPrefixMsg = "`setPrefix [p]`: Sets prefix to `p`."
    cleanMsg = "`clean`: Deletes all bot messages in a channel."

    joinMsg = "`join [name] [i]`: Adds a combatant as `name` to the combat order with `i` for their initiative roll."
    killMsg = "`kill [name]`: Deletes the combatant `name` if they exist in the combat order."
    beginMsg = "`begin`: Begins combat, and tags the first player in combat."
    endMsg = "`end`: Ends combat, and clears the tracker of all player information."
    nextMsg = "`next`: Moves onto the next player in combat."
    prevMsg = "`previous`: Moves back to the previous player in combat. (Alias: `prev`)"
    showMsg = "`show`: Shows full combat order."

    rollMsg1 = "`roll | roll [dice]`: Without any parameters, this rolls a 1d20. With an integer `dice`, it rolls one `dice`-sided dice."
    rollMsg2 = "`roll [quantity] d [dice] + [mod] + ...`: Rolls all specified `[quantity] d [dice]`, and adds any `mod`s."
    rollMsg3 = "`roll [adv / dis] [mod]`: Rolls two d20s and takes the higher or lower result depending on `adv` or `dis`. If it is given, adds the `mod`."
    whisperMsg = "`whisper [mention] [roll info]`: Sends a DM to the user you @`mention`ed in with the `roll` information."

    if arg == '':
        msg = "**Commands**" + "\n" + helpMsg + "\n" + "\n" + setPrefixMsg + "\n" + cleanMsg
        msg += "\n\n" + joinMsg + "\n" + killMsg + "\n" + beginMsg + "\n" + endMsg + "\n" + nextMsg + "\n" + prevMsg + "\n" + showMsg
        msg += "\n\n" + rollMsg1 + "\n" + rollMsg2  + "\n" + rollMsg3 + "\n" + whisperMsg
    elif arg in ['prefix', 'setPrefix']:
        msg = setPrefixMsg
    elif arg in ['initiative', 'join', 'begin', 'show']:
        msg = joinMsg + "\n" + beginMsg + "\n" + showMsg
    elif arg in ['stop', 'end', 'kill', 'delete']:
        msg = killMsg + "\n" + endMsg
    elif arg in ['next', 'prev', 'previous']:
        msg = nextMsg + "\n" + prevMsg
    elif arg in ['dice', 'roll', 'whisper', 'adv', 'dis', 'advantage', 'disadvantage']:
        msg = rollMsg1 + "\n" + rollMsg2 + "\n" + rollMsg3 + "\n" + whisperMsg
    else:
        msg = "⚠️ `" + arg + "` doesn't exist. Use `!help` for complete list of commands."
        
    msg = msg + "\n\n" + "Prefix: `" + str(p) + "`"
    await ctx.send(msg)

@bot.command()
async def clean(ctx):    
    def is_bot(m):
        return m.author == bot.user

    # Delete command message.
    await ctx.message.delete()

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
        await ctx.send("⚠️ To join initiative, the input must be in the form: `[name] [initiative roll]`.")
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
        await show(ctx)

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
        await ctx.send("⚠️ Initiative tracker hasn't been instantiated.\nUse `!join [name] [i]` to add a combatant to initiative.")

    msg = tracker.kill(name)
    await ctx.send(username.mention + " " + msg)
    await show(ctx)

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
        await ctx.send("⚠️ Initiative tracker hasn't been instantiated.\nUse `join [name] [i]` to add a combatant to initiative.")

    result = tracker.begin()
    botMessage = await ctx.send(result)
    tracker.last_message = botMessage

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
        await ctx.send("⚠️ Initiative tracker hasn't been instantiated.\nUse `join [name] [i]` to add a combatant to initiative.")
    
    await tracker.last_message.remove_reaction("⏮️", bot.user)
    await tracker.last_message.remove_reaction("⏭️", bot.user)

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
        await ctx.send("⚠️ Initiative tracker hasn't been instantiated.\nUse `join [name] [i]` to add a combatant to initiative.")

    result = tracker.next()
    botMessage = await ctx.send(result)
    tracker.last_message = botMessage

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
        await ctx.send("⚠️ Initiative tracker hasn't been instantiated.\nUse `join [name] [i]` to add a combatant to initiative.")
        
    result = tracker.prev()
    botMessage = await ctx.send(result)
    tracker.last_message = botMessage

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
        await ctx.send("⚠️ Initiative tracker hasn't been instantiated.\nUse `join [name] [i]` to add a combatant to initiative.")
        return
    
    if tracker.last_message != None:
        await tracker.last_message.remove_reaction("⏮️", bot.user)
        await tracker.last_message.remove_reaction("⏭️", bot.user)

    result = tracker.printTracker()
    botMessage = await ctx.send(result)
    tracker.last_message = botMessage

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

    current = tracker.trackerInfo[tracker.currentPlayer][0]

    if user == current and tracker.last_message.id == message_id:
        await tracker.last_message.remove_reaction("⏮️", bot.user)
        await tracker.last_message.remove_reaction("⏭️", bot.user)

        if emoji == "⏮️":
            await prev(channel)
        elif emoji == "⏭️":
            await next(channel)
        else:
            return

# ----------------------------------------------------------------------------------------------------
#                                              ROLLING
# ----------------------------------------------------------------------------------------------------

@bot.command()
async def roll(ctx, *arg):
    ''' Rolls dice. '''

    # Delete command message.
    await ctx.message.delete()

    if type(arg[0]) == tuple:
        arg = arg[0]

    arg = diceRoll.splitMe(arg)
    username = ctx.message.author
    normal = True

    print(arg)

    output = ""
    total = 0
    totalMsg = "\n**Total:** "
    has_error = False

    # Default roll
    if arg == []:
        res = diceRoll.roll()
    # Only dice size given
    elif len(arg) == 1:
        if arg[0] == 'adv':
            res = diceRoll.rollAdv(True)
        elif arg[0] == 'dis':
            res = diceRoll.rollAdv(False)
        elif "d" in arg[0]:
            res = diceRoll.complexRoll(arg[0])
        else:
            res = diceRoll.roll(arg[0])
    # Complex roll!
    else:
        if arg[0] == 'adv':
            if arg[1] == '+':
                mod = int(arg[2])
                res = diceRoll.rollAdv(True, mod)
            elif arg[1] == '-':
                mod = - int(arg[2])
                res = diceRoll.rollAdv(True, mod)
            else:
                res = ["⚠️ To roll with advantage, your input must be of the form: `adv +/- [mod]`.", 0, True]
        elif arg[0] == 'dis':
            if arg[1] == '+':
                mod = int(arg[2])
                res = diceRoll.rollAdv(False, mod)
            elif arg[1] == '-':
                mod = - int(arg[2])
                res = diceRoll.rollAdv(False, mod)
            else:
                res = ["⚠️ To roll with disadvantage, your input must be of the form: `dis +/- [mod]`.", 0, True]
        else:
            res = diceRoll.complexRoll(arg)

    output = res[0]
    total = res[1]
    has_error = res[2]

    if has_error:
        await ctx.send(username.mention + ' 🎲\n' + output)
    else:
        await ctx.send(username.mention + ' 🎲\n' + output + totalMsg + str(total))

@bot.command()
async def r(ctx, *arg):
    await roll(ctx, arg)

@bot.command()
async def froll(ctx, *arg):
    ''' Fudges a 1d20 roll. '''

    # Delete command message.
    await ctx.message.delete()

    if "DM" not in [r.name for r in ctx.message.author.roles]:
        fString = "This is a fudged roll. (You tried, buddy.)\nYou need to have the `DM` Role to be able to use this feature.\n\n"
    else:
        fString = ""

    username = ctx.message.author
    output = "**Result:** 1d20 "
    totalMsg = "\n**Total:** "

    if len(arg) == 2:
        res = diceRoll.fudgeMod(arg[0], arg[1])
        if res[2] == True:
            await ctx.send(res[0])
            return
        else:
            total = res[1]
            output += res[0]
    elif len(arg) == 1:
        res = diceRoll.fudge(arg[0])
        if res[2] == True:
            await ctx.send(res[0])
            return
        else:
            total = res[1]
            output += res[0]
    else:
        await ctx.send("Oops! Did you cast confusion? We couldn't parse your input!")

    await ctx.send(username.mention + ' 🎲\n' + fString + output + totalMsg + str(total))

@bot.command()
async def whisper(ctx, *arg):
    ''' Sends results to the people mentioned, and yourself. '''

    # Delete command message.
    await ctx.message.delete()

    sender = ctx.message.author
    recipients = ctx.message.mentions

    totalMsg = "\n**Total:** "

    params = arg[len(recipients):]
    rollInfo = diceRoll.complexRoll(params)

    output = rollInfo[0]
    total = rollInfo[1]
    has_error = rollInfo[2]

    if has_error:
        await ctx.send(sender.mention + " " + output)  
        return

    if sender.dm_channel == None:
        await sender.create_dm()
    sender_channel = sender.dm_channel  
    
    for recipient in recipients:
        if recipient.dm_channel == None:
            await recipient.create_dm()
        channel = recipient.dm_channel

        await channel.send(sender.display_name + " whispered a roll to you. 🎲\n" + output + totalMsg + str(total))
    
    await sender_channel.send("You whispered a roll to the following people: `" + str([r.display_name for r in recipients]) + "`.\n" + output + totalMsg + str(total))

bot.run(TOKEN)
