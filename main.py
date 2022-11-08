import asyncio
import discord
import pygsheets
import time

from config import TOKEN, GAME, INTENTS, SERVICE_FILE, SHEET, READY_CHANNEL, TEST_SERVER
from tiles import tile
from functions import upload, download

from discord.ui import Button, View
from discord.ext import commands

# Bot initialization
bot = commands.Bot(status=discord.Status.online, activity=GAME, intents=INTENTS)

# Sheet initialization
gc = pygsheets.authorize(service_file=SERVICE_FILE)
sheet = gc.open(SHEET)
wks = sheet[0]

# Commands
@bot.slash_command(description="Displays the current dashboard.")
async def dashboard(ctx):
    await ctx.defer()
    tileCount = int(wks.get_value('K5'))
    title = "**Displaying Dashboard**"
    ret = ""
    for row in range(tileCount):
        row = str(row+5)
        line = wks.get_value('B'+row) + ' (:' + wks.get_value('D'+row) + ':) - ' + wks.get_value('G'+row) + ' - ' + wks.get_value('I'+row)
        ret += line + "\n"
    await ctx.send_followup(embed=discord.Embed(title=title, description=ret))


@bot.slash_command(description="Reserves a tile under your name.")
async def reserve(ctx, tile_id: str):
    await ctx.defer()
    tileCount = int(wks.get_value('K5'))
    flag = False
    for row in range(tileCount):
        row = str(row+5)
        if wks.get_value('B'+row) == tile_id:
            flag = True
            wks.update_value('I'+row, ctx.author.display_name)
            break
    if not flag:
        newTile = tile(tile_id, "", "", "", ctx.author.display_name, "", "", "")
        upload(wks, newTile, tileCount + 5)
    await ctx.send_followup(embed=discord.Embed(colour=discord.Colour.green(), title = "Tile " + tile_id + " successfully reserved!"))


@bot.slash_command(description="Claims a tile as yours.")
async def claim(ctx, tile_id: str, score: str):
    await ctx.defer()
    tileCount = int(wks.get_value('K5'))
    flag = False
    for row in range(tileCount):
        row = str(row+5)
        if wks.get_value('B'+row) == tile_id:
            flag = True
            claimedTile = download(wks, row)
            claimedTile.owner = ctx.author.display_name
            claimedTile.status = 'Captured'
            claimedTile.expiry = '<t:' + str(100800 + time.time()) + ':R>'
            claimedTile.score = score
            upload(wks, claimedTile, row)
            break
    if not flag:
        newTile = tile(tile_id, "", "", 'Captured', ctx.author.display_name, score, '<t:' + str(int(100800 + time.time())) + ':R>', "")
        upload(wks, newTile, tileCount + 5)
    await ctx.send_followup(embed=discord.Embed(colour=discord.Colour.green(), title = "Tile " + tile_id + " successfully claimed!", description = "Score: " + score))

#test commands
@bot.slash_command(description="creates and displays a test tile", guild_ids = [TEST_SERVER])
async def testtile(ctx):
    testTile = tile("AAF", "Relic", "FlintTips", "Neutral", "210577", "1", "<t:00000000000:R>", "")
    await ctx.respond(embed=testTile.return_embed())

@bot.slash_command(description="uploads data of a test tile to sheet", guild_ids = [TEST_SERVER])
async def write(ctx):
    await ctx.defer()
    testTile = tile("AAF", "Relic", "FlintTips", "Neutral", "210577", "1", "<t:00000000000:R>", "")
    upload(wks, testTile, 5)
    await ctx.send_followup("hi")


@bot.slash_command(description="reads a tile", guild_ids = [TEST_SERVER])
async def read(ctx, row: int):
    await ctx.defer()
    fetchedTile = download(wks, row)
    await ctx.send_followup(embed=fetchedTile.return_embed())

# On ready
@bot.event
async def on_ready():
    ready_channel = bot.get_channel(READY_CHANNEL)
    ready_embed = discord.Embed(colour=discord.Colour.green(), title="Contested Territory Bot Active!", description = "version 0.1 by 210577")
    await ready_channel.send(embed=ready_embed)

bot.run(TOKEN)