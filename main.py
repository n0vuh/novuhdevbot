import discord
from discord.ext import commands
from cogs.ticket import Ticket

bot = commands.Bot(">", help_command=None)

# ADD COGS
bot.add_cog(Ticket(bot))

@bot.event
async def on_ready():
    print("Bot online.")

# GITHUB
bot.run( ${{ secrets.BOT_TOKEN }} )