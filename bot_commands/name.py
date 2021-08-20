from discord.ext import commands
from discord.ext.commands.context import Context
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from run import TTSBotSample


class Name(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # type: TTSBotSample

    @commands.command()
    async def name(self, ctx: Context):
        if ctx.guild is None:
            await ctx.channel.send("サーバー内専用コマンドです。")
            return
        split_message: List[str] = ctx.message.content.split(" ")
        if len(split_message) == 2:
            if split_message[1] == "on":
                name_speech = True
            elif split_message[1] == "off":
                name_speech = False
            else:
                await ctx.channel.send("名前読み上げ設定が不正です。onかoffで設定してください。")
                return
            self.bot.set_name_speech(ctx.guild.id, name_speech)
            await ctx.channel.send(f"名前読み上げ設定を{split_message[1]}に設定しました。")
        elif len(split_message) == 1:
            name_speech = self.bot.get_name_speech(ctx.guild.id)
            if name_speech is None:
                name_speech = True
            await ctx.channel.send(f"現在の名前読み上げ設定は{'on' if name_speech else 'off'}です。")
        else:
            await ctx.channel.send("コマンドが不正です。")
