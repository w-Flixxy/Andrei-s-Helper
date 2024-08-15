import discord
from discord import app_commands
from discord.ext import commands
from typing import *

class BanCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, interaction:discord.Interaction, user:discord.Member, reason:  Optional[str] = None):
        # getting position of highest role of the user who wants to ban
        highest_role_m = interaction.user.roles[-1] if interaction.user.roles else None
        highest_role_pos_m = highest_role_m.position

        log_channel = self.client.get_channel(1269281817354047551)

        # getting position of highest role of the user who gets baned
        highest_role_u = user.roles[-1] if user.roles else None
        highest_role_pos_u = highest_role_u.position

        if highest_role_pos_u > highest_role_pos_m:
            error_embed = discord.Embed(title = ":x: | An error occured.", colour=discord.colour.parse_hex_number("4344FF"))
            error_embed.add_field(name = "", value = f"```You cannot ban that user, as he has a higher role than you.```")
            await interaction.response.send_message(embed = error_embed, ephemeral=True)
            log_embed = discord.Embed(title = "", description = f"{interaction.user.mention} tried to ban {user.mention}", colour = discord.colour.parse_hex_number("B51000"))
            log_embed.add_field(name = "More Info:", value = f"{interaction.user.mention} | ``{interaction.user.id}``, tried to ban: {user.mention} | ``{user.id}``, but failed.")
            await log_channel.send(embed = log_embed)
            return
        
        if reason == None:
            reason = "Not Provided"
            await user.ban(reason = reason)
            await interaction.response.send_message(f"Succesfully baned {user.mention}", ephemeral=True)
        else:
            print(reason)
            await user.ban(reason = reason)
            await interaction.response.send_message(f"Succesfully baned {user.mention} with reason {reason}", ephemeral=True)
        
        log_embed = discord.Embed(title = "", description = f"{interaction.user.mention} baned {user.mention}", colour = discord.colour.parse_hex_number("35DB00"))
        log_embed.add_field(name = "More Info:", value = f"{user.mention} | ``{user.id}``, was baned by {interaction.user.mention} | {interaction.user.id}")

        await log_channel.send(embed = log_embed)

    @ban.error
    async def ban_error(self, interaction:discord.Interaction, error):
        error_embed = discord.Embed(title = ":x: | An error occured.", colour=discord.colour.parse_hex_number("4344FF"))
        error_embed.add_field(name = "", value = f"```{error}```")
        await interaction.response.send_message(embed = error_embed, ephemeral=True)

async def setup(client):
    await client.add_cog(BanCommand(client))