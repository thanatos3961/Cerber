import sys
sys.stdout.reconfigure(encoding='utf-8')

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import token_cgb
import os

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=".", owner_id=678456343413260307, intents=intents)

MY_GUILD = nextcord.Object(id=1281710386126782569)

Denied_emoji = "❌"
Checkmark_emoji = "✔"

embed_color = nextcord.Color.blue()
unsuccessful_color = nextcord.Color.orange()

bot.remove_command("help")

# Path to your credentials JSON file
creds_path = os.path.join(os.path.dirname(__file__), 'cerber-435722-877304fe22e4.json')

# Define the scope of the API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

# Open the Google Sheet by name
sheet = client.open("CGB POINT SHEET").sheet1  # Use the name of your sheet

def award_point(username, points):
    try:
        cell = sheet.find(username)
        
        if cell is not None:
            current_score = int(sheet.cell(cell.row, cell.col + 4).value)
            new_score = current_score + points
            
            sheet.update_cell(cell.row, cell.col + 4, new_score)
            print(f"Awarded 1 point to {username}. New score: {new_score}")
        else:
            return

    except gspread.exceptions.GSpreadException as e:
        print(f"An error occurred while trying to update the sheet: {e}")



@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    guild_count = len(bot.guilds)
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"Currently in {guild_count} guilds!"))
    cogs_path = os.path.join(os.path.dirname(__file__), 'cogs')
    for filename in os.listdir(cogs_path):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded extension: {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load extension {filename[:-3]}: {e}")


@bot.event
async def on_command_error(ctx, error):
    channel = ctx.channel
    if isinstance(error, commands.CommandNotFound):
        return
    else:
        embed = nextcord.Embed(
            title="Error log",
            description=f"An error occurred: {error}",
            color=nextcord.Color.dark_red()
        )
        await channel.send(embed=embed)


@bot.slash_command(name="add_points")
@commands.is_owner()
async def add_points(interaction: nextcord.Interaction, username: str, points: int = 1):
    award_point(username=username, points=points)
    word = "point"
    if points > 1:
        word = "points"
    await interaction.response.send_message(f"{points} {word} have been added to ", ephemeral=True)


# The modal class
class ExampleModal(nextcord.ui.Modal):
    def __init__(self, points):
        self.points = points
        super().__init__(title="Reporting", timeout=5 * 60)

        self.first = nextcord.ui.TextInput(
            label="Your Username:",
            placeholder="Enter your answer",
            required=True,
        )
        self.add_item(self.first)

        self.second = nextcord.ui.TextInput(
            label="Rulebreakers ROBLOX Username:",
            placeholder="Enter your answer",
            required=True,
        )
        self.add_item(self.second)

        self.third = nextcord.ui.TextInput(
            label="Report Reason",
            placeholder="Enter your reason",
            required=True,
        )
        self.add_item(self.third)

        self.fourth = nextcord.ui.TextInput(
            label="Evidence",
            placeholder="Enter your answer",
            required=True,
        )
        self.add_item(self.fourth)

        self.fifth = nextcord.ui.TextInput(
            label="Any Additional Info",
            placeholder="Enter your answer",
            required=False,
        )
        self.add_item(self.fifth)

    async def callback(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="New Report",
            description="A report has been submitted"
        )
        award_point(self.first.value, points=self.points)
        embed.add_field(name="Reporter's Username:", value=self.first.value, inline=False)
        embed.add_field(name="Rulebreakers ROBLOX Username:", value=self.second.value, inline=False)
        embed.add_field(name="Reason:", value=self.third.value, inline=False)
        embed.add_field(name="Evidence:", value=self.fourth.value, inline=False)
        embed.add_field(name="Additional Info", value=self.fifth.value, inline=False)
        
        channel = interaction.guild.get_channel(1284792540670726165)
        await channel.send(embed=embed)
        await interaction.response.send_message("Submitted, thanks for reporting.", ephemeral=True)



class HRReportButton(nextcord.ui.Button): # HR
    def __init__(self):
        super().__init__(label="Submit HR Report", style=nextcord.ButtonStyle.primary)

    async def callback(self, interaction: nextcord.Interaction):
        points = 8
        modal = ExampleModal(points)
        await interaction.response.send_modal(modal)

class HRReportView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HRReportButton())



class LRReport(nextcord.ui.Button): # LR
    def __init__(self):
        super().__init__(label="Submit LR Report", style=nextcord.ButtonStyle.primary)

    async def callback(self, interaction: nextcord.Interaction):
        points = 2
        modal = ExampleModal(points)
        await interaction.response.send_modal(modal)

class LRReportView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(LRReport())


class ExploitReport(nextcord.ui.Button): # LR
    def __init__(self):
        super().__init__(label="Submit LR Report", style=nextcord.ButtonStyle.primary)

    async def callback(self, interaction: nextcord.Interaction):
        points = 2
        modal = ExampleModal(points)
        await interaction.response.send_modal(modal)



class ExploitReport(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(LRReport())



@bot.slash_command(name="send_report_button")
@commands.is_owner()
async def send_report_button(interaction: nextcord.Interaction):
    """Sends a persistent message with a button to open the report modal."""
    embed = nextcord.Embed(
        title="HR Report Module",
        description="Click the button below to submit a report.\n After submitting the report, you get points. You must use your roblox username.\n(MAKE SURE YOUR USERNAME IS EXACT)"
    )
    embed.add_field(name="CGB Points Tracker", value="https://docs.google.com/spreadsheets/d/1EMlj673kmX7bBO86bgtgE6ekasf5Gy2esxVZQmaJb90/edit?usp=sharing")
    view = HRReportView()  # Create the view with the button
    channel = interaction.guild.get_channel(1284792112633876550)  # Set to the channel ID where you want to send the button
    await channel.send(embed=embed, view=view)  
    await interaction.response.send_message("Report button has been sent!", ephemeral=True)

@bot.slash_command(name="send_lr_report_button")
@commands.is_owner()
async def send_report_button(interaction: nextcord.Interaction):
    """Sends a persistent message with a button to open the report modal."""
    embed = nextcord.Embed(
        title="LR Report Module",
        description="Click the button below to submit a report.\n After submitting the report, you get points. You must use your roblox username.\n(MAKE SURE YOUR USERNAME IS EXACT)"
    )
    embed.add_field(name="CGB Points Tracker", value="https://docs.google.com/spreadsheets/d/1EMlj673kmX7bBO86bgtgE6ekasf5Gy2esxVZQmaJb90/edit?usp=sharing")
    view = LRReportView()  # Create the view with the button
    channel = interaction.guild.get_channel(1284792112633876550)  # Set to the channel ID where you want to send the button
    await channel.send(embed=embed, view=view)  
    await interaction.response.send_message("Report button has been sent!", ephemeral=True)


@bot.slash_command(name="send_exploit_report")
@commands.is_owner()
async def send_report_button(interaction: nextcord.Interaction):
    """Sends a persistent message with a button to open the report modal."""
    embed = nextcord.Embed(
        title="Exploit Report Module",
        description="Click the button below to submit an exploit report.\n After submitting the report, you get     points. You must use your roblox username.\n(MAKE SURE YOUR USERNAME IS EXACT)"
    )
    embed.add_field(name="CGB Points Tracker", value="https://docs.google.com/spreadsheets/d/1EMlj673kmX7bBO86bgtgE6ekasf5Gy2esxVZQmaJb90/edit?usp=sharing")
    view = LRReportView()  # Create the view with the button
    channel = interaction.guild.get_channel(1284792112633876550)  # Set to the channel ID where you want to send the button
    await channel.send(embed=embed, view=view)  
    await interaction.response.send_message("Report button has been sent!", ephemeral=True) 


@bot.command(name='reload', description="Reloads a cog.")
@commands.is_owner()
async def reload(ctx: commands.Context, cog_name: str):
    if ctx.author.id != 678456343413260307:
        await ctx.send("You aren't the owner of this bot.", ephemeral=True)
        return
    try:
        await bot.reload_extension(f"cogs.{cog_name}")
        embed = nextcord.Embed(
            title="Cog Reloaded",
            description=f"Successfully reloaded the cog `{cog_name}`.",
            color=nextcord.Color.dark_green()
        )
        await ctx.send(embed=embed, ephemeral=True)
    except Exception as e:
        embed = nextcord.Embed(
            title="Error",
            description=f"Failed to reload the cog `{cog_name}`: {str(e)}",
            color=nextcord.Color.dark_red()
        )
        await ctx.send(embed=embed, ephemeral=True)


@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx: commands.Context):
    if ctx.author.id != 678456343413260307:
        await ctx.send("You aren't the owner of this bot.", ephemeral=True)
    guild = ctx.guild
    await bot.sync_all_application_commands()
    guild_count = len(bot.guilds)
    print(f"Commands synced for guild: {guild} ({guild.id})")
    embed = nextcord.Embed(
        title=None,
        description=f"{Checkmark_emoji} | Synced all commands for {guild_count} guilds.",
        color=nextcord.Color.dark_green()
    )
    timestamp = datetime.now().strftime("%I:%M %p")
    embed.set_footer(text=timestamp)
    await ctx.send(embed=embed)


bot.run(token_cgb.tokenval)
