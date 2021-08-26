from discord.ext import commands
from discord.ext.commands.context import Context
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from run import TTSBotSample


class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # type: TTSBotSample

    @commands.command()
    async def stop(self, ctx: Context):
        if ctx.guild is None:
            await ctx.channel.send("サーバー内専用コマンドです。")
            return
        connection = self.bot.connections.get(ctx.guild.id)
        if connection is None:
            await ctx.channel.send(f"{self.bot.user.name}は現在TTS機能が起動していません。")
            return
        await self.bot.text_to_speech(connection, "TTS機能を終了します。", tts_end=True)

def setup(bot):
    bot.add_cog(Stop(bot))
