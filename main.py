import discord
import os
from discord.ext import commands
from discord import app_commands

client = commands.Bot(command_prefix="py!", intents = discord.Intents.all())

@client.event
async def on_ready():
    print(client.user.name)
    print(client.user.id)
    print(client.user)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(client.guilds)} servers!"))
    for filename in os.listdir("cogs"):
        print(filename)
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

@client.command()
@commands.is_owner()
async def sync(ctx):
    await client.tree.sync()
    await ctx.send("Succesfully synced slash commands!")

@commands.is_owner()
@client.command()
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    print(f"Loaded: cogs.{extension}")
    await ctx.send(f"Succesfully loaded `cogs.{extension}`!")

@commands.is_owner()
@client.command()
async def unload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    print(f"Unloaded: cogs.{extension}")
    await ctx.send(f"Succesfully unloaded `cogs.{extension}`!")

@commands.is_owner()
@client.command(aliases=["rl"])
async def reload(ctx, extension):
    if extension == "all":
        for filename in os.listdir("T-Security/cogs"):
            if filename.endswith(".py"):
                await client.unload_extension(f"cogs.{filename[:-3]}")
        for filename in os.listdir("T-Security/cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send("Succesfully reloaded all cog files.")
    else:
        await client.unload_extension(f"cogs.{extension}")
        await client.load_extension(f"cogs.{extension}")
        await ctx.send(f"Succesfully reloaded `cogs.{extension}`!")

client.run(token = "TOKEN")