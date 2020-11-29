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

# Create the Initiative Tracker object.
tracker = InitTracker()

@bot.command()
async def join(ctx, *arg):
    if len(arg) < 2:
        await ctx.send("To join initiative, the input must be in the form: `[name] [initiative roll]`.")
    else:
        username = ctx.message.author
        name = " ".join(arg[:-1])
        initRoll = arg[-1]

        msg = tracker.join(username, name, initRoll)
        await ctx.send(username.mention + " " + msg)

@bot.command()
async def begin(ctx):
    msg = tracker.begin()
    username = tracker.trackerInfo[tracker.currentPlayer][0]
    await ctx.send(username.mention + "\n" + msg)

@bot.command()
async def end(ctx):
    msg = tracker.end()
    await ctx.send(msg)

@bot.command()
async def next(ctx):
    msg = tracker.next()
    username = tracker.trackerInfo[tracker.currentPlayer][0]
    await ctx.send(username.mention + "\n" + msg)

@bot.command()
async def prev(ctx):
    msg = tracker.prev()
    username = tracker.trackerInfo[tracker.currentPlayer][0]
    await ctx.send(username.mention + "\n" + msg)

@bot.command()
async def show(ctx):
    msg = tracker.printTracker()
    await ctx.send(msg)