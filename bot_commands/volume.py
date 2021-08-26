from discord.ext import commands
from discord.ext.commands.context import Context
from typing import TYPE_CHECKING, List

from bot_lib.common import DEFAULT_VOLUME

if TYPE_CHECKING:
    from run import TTSBotSample


class Volume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # type: TTSBotSample

    @commands.command()
    async def volume(self, ctx: Context):
        if ctx.guild is None:
            await ctx.channel.send("サーバー内専用コマンドです。")
            return
        split_message: List[str] = ctx.message.content.split(" ")
        if len(split_message) == 2:
            try:
                volume = int(split_message[1])
                if volume < 0 or 100 < volume:
                    await ctx.channel.send("音量の範囲が不正です。1～100での整数値で設定してください。")
                    return
            except Exception:
                await ctx.channel.send("音量の値が不正です。1～100での整数値で設定してください。")
                return
            self.bot.set_volume(ctx.guild.id, volume)
            await ctx.channel.send(f"音量を{volume}に設定しました。")
        elif len(split_message) == 1:
            volume = self.bot.get_volume(ctx.guild.id)
            if volume is None:
                volume = DEFAULT_VOLUME
            await ctx.channel.send(f"現在の音量は{volume}です。")
        else:
            await ctx.channel.send("コマンドが不正です。")


def setup(bot):
    bot.add_cog(Volume(bot))
