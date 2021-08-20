from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from run import TTSBotSample


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # type: TTSBotSample

    @commands.command()
    async def help(self, ctx: Context):
        embed = Embed(
            title="**VOICEVOX ENGINE + Discord TTS Bot**",
            description="VOICEVOX ENGINEを音声合成エンジンとして利用しているTTS(Text-to-Speech) Botです。",
        )
        embed.add_field(
            name="__**?help**__",
            value="このヘルプを表示します。",
            inline=False
        )
        embed.add_field(
            name="__**?metan**__",
            value="四国めたんの声でチャンネルのコメントを読み上げます。",
            inline=False
        )
        embed.add_field(
            name="__**?zundamon**__",
            value="ずんだもんの声でチャンネルのコメントを読み上げます。",
            inline=False
        )
        embed.add_field(
            name="__**?volume**__",
            value="音声再生時の音量が見られます。",
            inline=False
        )
        embed.add_field(
            name="__**?volume**__ <value>",
            value="音声再生時の音量を調節できます。音量(value)は1～100で指定してください。",
            inline=False
        )
        embed.add_field(
            name="__**?name**__",
            value="テキスト読み上げの際に、ユーザー名を読み上げるか否かの設定が見られます。",
            inline=False
        )
        embed.add_field(
            name="__**?name**__ on/off",
            value="テキスト読み上げの際に、ユーザー名を読み上げるか否かの設定ができます。onかoffのどちらかを選んでください。",
            inline=False
        )
        embed.add_field(
            name="__**?end**__",
            value="コメントの読み上げを終了します(四国めたん・ずんだもん共通の終了コマンドです)。",
            inline=False
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url_as(format='png', size=1024))
        embed.set_footer(text="VOICEVOX ENGINE + Discord TTS Bot",
                         icon_url=self.bot.user.avatar_url_as(format='png', size=256))

        await ctx.channel.send(embed=embed)
