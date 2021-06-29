import discord, random, string
from discord.ext import commands
from asyncio import sleep

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.opened = dict()

    @commands.cooldown(1, 10, commands.cooldowns.BucketType.member)
    @commands.command(aliases=["openticket", "ticket", "open_ticket", "createticket"])
    async def create_ticket(self, ctx: commands.Context, *, query: str):
        """
        Opens a support ticket.
        """
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        if ctx.message.author not in self.opened:
            channel_name = f"ticket-" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
            channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)

            embed=discord.Embed(description=f'View your ticket @ <#{channel.id}>', color=0xba47fe)
            embed.set_author(name=f"Support Ticket Opened")
            embed.add_field(name="Query", value=query)

            await ctx.message.author.send(embed=embed)

            embed=discord.Embed(title="Support Ticket", description=f'{ctx.message.author.mention} asked, "{query}"', color=0xba47fe)
            embed.set_author(name=f"{channel_name}")
            embed.set_footer(text="Close this ticket with >close")

            await channel.send("<@&851987287913922610>", embed=embed)

            mapping = {channel.id: {
                "author": ctx.message.author,
                "query": query,
                "channel": channel_name
            }}
            self.opened.update(
                mapping
            )
        else:
            await ctx.send(f"Sorry {ctx.message.author.mention}, you already have a ticket open.")

    @commands.command()
    async def close(self, ctx):
        if ctx.message.channel.id in self.opened:
            await ctx.send("Closing...")
            await sleep(3)
            embed=discord.Embed(color=0xba47fe)
            embed.set_author(name="Support Ticket Closed")
            embed.add_field(name="Closed by:", value="You" if ctx.message.author is not self.opened[ctx.message.channel.id]["author"].id else ctx.message.author.name.mention, inline=True)
            await ctx.message.channel.delete()
            await ctx.message.author.send(embed=embed)

    # @commands.has_role(851987287913922610)
    @commands.command(aliases=["sclose", "sc", "staffclose"])
    async def supportclose(self, ctx, *, reason: str):
        if "ticket" in ctx.channel.name:
            await ctx.send("Support has closed this ticket...")
            await sleep(3)
            embed=discord.Embed(color=0xba47fe)
            embed.set_author(name="Support Ticket Closed")
            embed.description = f'({self.opened[ctx.channel.id]["channel"]})'
            embed.add_field(name="Reason:", value=f'*"{reason}"*', inline=True)
            embed.add_field(name="Closed by:", value=f"*{ctx.message.author}*", inline=True)
            await self.opened[ctx.channel.id]["author"].send(embed=embed)
            await ctx.channel.delete()


    # @commands.has_role(851987287913922610)
    # @commands.command