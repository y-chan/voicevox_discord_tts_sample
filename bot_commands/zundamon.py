from discord.ext import commands
from discord.ext.commands.context import Context

from bot_lib.common import TTSStartCommon


class Zundamon(TTSStartCommon):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command()
    async def zundamon(self, ctx: Context):
        await self.tts_setup(ctx, 1)


def setup(bot):
    bot.add_cog(Zundamon(bot))
