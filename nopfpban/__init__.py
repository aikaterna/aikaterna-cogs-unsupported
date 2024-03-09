from redbot.core import commands

from .nopfpban import NoPfpBan

__red_end_user_data_statement__ = "This cog does not persistently store data or metadata about users."


async def setup(bot: commands.Bot):
    n = NoPfpBan(bot)
    await bot.add_cog(n)
