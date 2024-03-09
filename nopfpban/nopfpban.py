import discord
import logging

from redbot.core import commands, Config


log = logging.getLogger("red.aikaterna.nopfpban")


class NoPfpBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2706371337)
        default_guild_settings = {"autoban_enabled": False, "autoban_reason": "Automated ban: No profile picture"}
        self.config.register_guild(**default_guild_settings)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        autoban_enabled = await self.config.guild(member.guild).autoban_enabled()
        autoban_reason = await self.config.guild(member.guild).autoban_reason()
        if autoban_enabled and not member.avatar:
            try:
                await member.ban(reason=autoban_reason)
            except discord.Forbidden:
                log.info("NoPfpBan cog does not have permissions to van in guild {member.guild.id}")

    @commands.group()
    async def autoban(self, ctx):
        """Manage autoban settings."""
        pass

    @autoban.command()
    async def enable(self, ctx):
        """Enable autoban in this guild for users with no profile picture."""
        await self.config.guild(ctx.guild).autoban_enabled.set(True)
        await ctx.send("Autoban enabled in this guild.")

    @autoban.command()
    async def disable(self, ctx):
        """Disable autoban in this guild for users with no profile picture."""
        await self.config.guild(ctx.guild).autoban_enabled.set(False)
        await ctx.send("Autoban disabled in this guild.")

    @autoban.command()
    async def reason(self, ctx, *, reason: str):
        """
        Set the automatic ban reason, for this guild.
        It will show in the audit log as the reason for removing the user.
        """
        await self.config.guild(ctx.guild).autoban_reason.set(reason)
        await ctx.send(f"Autoban audit log reason set to: `{reason}`")

    @autoban.command()
    async def status(self, ctx):
        """Check the status of autoban."""
        autoban_enabled = await self.config.guild(ctx.guild).autoban_enabled()
        await ctx.send(f"Autoban is {'enabled' if autoban_enabled else 'disabled'} in this guild.")
