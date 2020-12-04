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
    guild = msg.guild
    if p.prefixInfo == []:
        return "!"
    else:
        return p.getPrefix(guild)

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

    rollMsg1 = "`roll | roll [dice]`: Without any parameters, this rolls a 1d20. With an integer `dice`, it rolls a 1d`[dice]`."
    rollMsg2 = "`roll [quantity] d [dice] + [mod] + ...`: Rolls all specified `[quantity] d [dice]`, and adds any `mod`s."
    gmrollMsg = "`gmroll [mention] [roll info]`: Sends a DM to the user you @`mention`ed in with the `roll` information."

    if arg == '':
        msg = "**Commands**" + "\n" + helpMsg + "\n" + prefixMsg + "\n" + setPrefixMsg + "\n" + cleanMsg
        msg += "\n\n" + joinMsg + "\n" + killMsg + "\n" + beginMsg + "\n" + endMsg + "\n" + nextMsg + "\n" + prevMsg + "\n" + showMsg
        msg += "\n\n" + rollMsg1 + "\n" + rollMsg2  + "\n" + gmrollMsg
    elif arg in ['prefix', 'setPrefix']:
        msg = prefixMsg + "\n" + setPrefixMsg
    elif arg in ['initiative', 'join', 'begin', 'show']:
        msg = joinMsg + "\n" + beginMsg + "\n" + showMsg
    elif arg in ['stop', 'end', 'kill', 'delete']:
        msg = killMsg + "\n" + endMsg
    elif arg in ['next', 'prev', 'previous']:
        msg = nextMsg + "\n" + prevMsg
    elif arg in ['dice', 'roll', 'gmroll']:
        msg = rollMsg1 + "\n" + rollMsg2 + "\n" + gmrollMsg
    else:
        msg = "⚠️ `" + arg + "` doesn't exist. Use `!help` for complete list of commands."
        
    msg = msg + "\n\n" + "Prefix: `" + p + "`"
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

    # If being called from somewhere else...
    if len(arg) != 0 and type(arg[0]) == tuple:
        name = arg[0][1]
        arg = splitMe(arg[0][0])
        normal = False
    # If normal roll...
    else:
        # Delete command message.
        await ctx.message.delete()
    
        arg = splitMe(arg)
        username = ctx.message.author
        normal = True

    output = ""
    total = 0
    totalMsg = "\n**Total:** "
    has_error = False

    # Default roll
    if arg == []:
        res = diceRoll.roll()
        output += res[0]
        total = res[1]
        has_error = res[2]
    # Only dice size given
    elif len(arg) == 1 and "d" not in arg[0]:
        res = diceRoll.roll(arg[0])
        output += res[0]
        total = res[1]
        has_error = res[2]
    # Complex roll!
    else:
        output += "**Result:** "
        is_subtract = False

        # Handle each rolling chunk in the params.
        for i in range(len(arg)):
            # In the form [quantity]d[dice]
            if "d" in arg[i]:
                params = arg[i].split("d")
                q = params[0]
                d = params[1]

                if q == '':
                    q = '1'

                res = diceRoll.multiroll(q, d)
                if res[2]:
                    has_error = True
                
                if res[1] != 0:
                    output += res[0]

                    if is_subtract:
                        total -= res[1]
                    else:
                        total += res[1]
                else:
                    await ctx.send("Oops! Did you cast confusion? We couldn't parse your input!")
                    return
            elif arg[i] == "+":
                output += " + "
                is_subtract = False
            elif arg[i] == "-":
                output += " - "
                is_subtract = True
            # It's a modifier.
            else:
                try:
                    res = int(arg[i])
                except ValueError:
                    await ctx.send("Oops! Did you cast confusion? We couldn't parse your input!")
                    return
                
                if res < 0:
                    output += " - " + str(-res)
                else:
                    output += arg[i]
                
                if is_subtract:
                        total -= res
                else:
                    total += res
    
    if has_error:
        await ctx.send(username.mention + ' 🎲\n' + output)
    elif not normal:
        await ctx.send(name + " whispered a roll to you. 🎲\n" + output + totalMsg + str(total))
    else:
        await ctx.send(username.mention + ' 🎲\n' + output + totalMsg + str(total))

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
async def gmroll(ctx, *arg):
    ''' Sends results to the person mentioned. '''

    # Delete command message.
    await ctx.message.delete()

    sender = ctx.message.author
    recipients = ctx.message.mentions

    if len(recipients) > 1:
        sender_channel = sender.dm_channel
        if sender_channel == None:
            sender_channel = sender.create_dm()
        
        await sender_channel.send("You're only allowed to whisper a roll to one person!")
        return

    params = []

    for item in arg[1:]:
        params.append(item)
    
    if recipients[0].dm_channel == None:
        await recipients[0].create_dm()
    channel = recipients[0].dm_channel
    
    await roll(channel, tuple([params, sender.display_name]))

def splitMe(arg):
    ''' HELPER FUNCTION: To split tuples into roll chunks. '''

    arg = "".join(arg)
    splitPlus = " + ".join(arg.split('+'))
    fullSplit = " - ".join(splitPlus.split('-')).split()

    return fullSplit

bot.run(TOKEN)
