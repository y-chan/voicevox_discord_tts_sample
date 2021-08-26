from discord.ext import commands
from discord.ext.commands.context import Context

from bot_lib.common import TTSStartCommon


class Metan(TTSStartCommon):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command()
    async def metan(self, ctx: Context):
        await self.tts_setup(ctx, 0)


def setup(bot):
    bot.add_cog(Metan(bot))
