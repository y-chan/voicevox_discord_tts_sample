from dataclasses import dataclass, field

from discord import VoiceClient
from discord.ext import commands
from discord.ext.commands.context import Context
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from run import TTSBotSample


@dataclass
class SpeechQueueItem:
    content: str
    username: str
    tts_end: Optional[bool] = False


@dataclass
class ConnectionItem:
    voice_client: VoiceClient
    channel_id: int
    speaker_id: int
    name_speech: bool
    volume: int
    speech_queue: Optional[List[SpeechQueueItem]] = field(default_factory=list)


DEFAULT_VOLUME = 50


class TTSStartCommon(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot  # type: TTSBotSample

    async def tts_setup(self, ctx: Context, speaker_id: int) -> None:
        if ctx.guild is None:
            await ctx.channel.send("サーバー内専用コマンドです。")
            return
        connection = self.bot.connections.get(ctx.guild.id)
        if connection is not None:
            await ctx.channel.send(f"既にこのサーバー内では{self.bot.user.name}が使用されています。")
            return
        if ctx.author.voice is None:
            await ctx.channel.send("まずはあなたがボイスチャンネルに接続してください。")
            return

        await ctx.author.voice.channel.connect()
        voice_client: VoiceClient = ctx.guild.voice_client
        volume = self.bot.get_volume(ctx.guild.id) or DEFAULT_VOLUME
        name_speech = self.bot.get_name_speech(ctx.guild.id)
        if name_speech is None:
            name_speech = True

        connection = ConnectionItem(
            voice_client,
            ctx.channel.id,
            speaker_id,
            name_speech,
            volume
        )
        self.bot.connections[ctx.guild.id] = connection
        await ctx.channel.send(f"{self.bot.user.name}をボイスチャンネルに接続し、TTS機能を起動しました。")
        await self.bot.text_to_speech(connection, "TTS機能を起動しました。")
