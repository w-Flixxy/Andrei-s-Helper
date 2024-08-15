import discord
from discord import app_commands
from discord.ext import commands
from typing import *
from datetime import datetime

class WarnCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Warns a user")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_txt = f"{user.id} | {reason} | {time_now}\n"
        with open("cogs/warns.txt", "a") as f:
            f.write(formatted_txt)

        warn_embed = discord.Embed(title="", description=f"Succesfully warned {user.mention} for {reason}", color = discord.colour.parse_hex_number("35DB00"))
        await interaction.response.send_message(embed=warn_embed, ephemeral=True)

    @warn.error
    async def warn_error(self, interaction: discord.Interaction, error):
        error_embed = discord.Embed(title = ":x: | An error occurred.", colour = discord.colour.parse_hex_number("4344FF"))
        error_embed.add_field(name="", value=f"```{error}```")
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @app_commands.command(description="Retrieves previous warnings for a user.")
    @app_commands.checks.has_permissions(manage_members = True)
    async def warns(self, interaction: discord.Interaction, user: discord.Member):
        look_for_id = str(user.id)
        warnings_found = []

        # Read the file and search for the user's warnings
        with open("cogs/warns.txt", "r") as f:
            content = f.read()
            individual_warns = content.splitlines()
            for text in individual_warns:
                splited_string = text.split(" | ")
                if len(splited_string) == 3 and look_for_id == splited_string[0]:  # Ensure proper format
                    warnings_found.append(splited_string)

        # Check if any warnings were found
        if warnings_found:
            embed = discord.Embed(description = f"Warnings for {user.name}",color = discord.colour.parse_hex_number("B51000"))
            for warn in warnings_found:
                reason = warn[1]
                date = warn[2]
                embed.add_field(name=f"Warn on {date}", value=reason, inline=False)
        else:
            embed = discord.Embed(description = f"No warnings found for {user.name}",color = discord.colour.parse_hex_number("35DB00"))

        await interaction.response.send_message(embed=embed)


async def setup(client):
    await client.add_cog(WarnCommands(client))
