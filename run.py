import argparse
import os
import sqlite3
from asyncio import sleep
from typing import List, Dict, Union

from discord import Game, Message, PCMVolumeTransformer, PCMAudio
from discord.ext import commands

try:
    import each_cpp_forwarder
except:
    from voicevox_engine.dev import each_cpp_forwarder

import romkan
import soundfile

from voicevox_engine.full_context_label import extract_full_context_label
from voicevox_engine.model import AccentPhrase, AudioQuery, Mora
from voicevox_engine.synthesis_engine import SynthesisEngine
from bot_lib.common import ConnectionItem, SpeechQueueItem

from bot_commands.metan import Metan
from bot_commands.zundamon import Zundamon
from bot_commands.name import Name
from bot_commands.volume import Volume
from bot_commands.end import End
from bot_commands.help import Help

# search_name = "/".join(str(__file__).split("/")[:-1]) + "/bot_commands/*.py"
# COMMANDS = list(
#     map(
#         lambda p: "." + p.replace("\\", ".").replace("C:/", "").replace("/", ".").replace(".py", ""),
#         glob.glob(search_name)
#     )
# )


def mora_to_text(mora: str):
    if mora == "cl":
        return "ッ"
    elif mora == "ti":
        return "ティ"
    elif mora == "tu":
        return "トゥ"
    elif mora == "di":
        return "ディ"
    elif mora == "du":
        return "ドゥ"
    else:
        return romkan.to_katakana(mora)


class TTSBotSample(commands.Bot):
    def __init__(self, command_prefix: str, use_gpu: bool) -> None:
        super().__init__(command_prefix)

        # TODO: VOICEVOX_DIR上だとこれが通用しない
        # for cog in COMMANDS:
        #     try:
        #         bot.load_extension(cog)
        #     except Exception:
        #         traceback.print_exc()
        self.remove_command("help")
        for cog in [Metan, Zundamon, Name, Volume, End, Help]:
            self.add_cog(cog(self))
        each_cpp_forwarder.initialize("1", "2", "3", use_gpu)
        self.engine = SynthesisEngine(
            yukarin_s_forwarder=each_cpp_forwarder.yukarin_s_forward,
            yukarin_sa_forwarder=each_cpp_forwarder.yukarin_sa_forward,
            decode_forwarder=each_cpp_forwarder.decode_forward,
        )
        self.connections: Dict[int, ConnectionItem] = {}
        self.con = sqlite3.connect("tts_bot.sqlite")
        self.cur = self.con.cursor()
        self.create_db()

    def __del__(self):
        self.con.close()

    async def on_ready(self):
        print(
            "Successful login.\n" +
            "Name: " + str(self.user.name) + "\n" +
            "ID: " + str(self.user.id)
        )
        await self.change_presence(activity=Game(name="?help"))

    async def on_message(self, message: Message) -> None:
        await self.process_commands(message)
        if message.content.startswith(self.command_prefix):
            return
        if message.author.bot or not message.guild:
            return
        connection = self.connections.get(message.guild.id)
        if connection is not None and connection.channel_id == message.channel.id:
            await self.text_to_speech(connection, message.content, message.author.name)

    def replace_mora_pitch(
        self, accent_phrases: List[AccentPhrase], speaker_id: int
    ) -> List[AccentPhrase]:
        return self.engine.extract_phoneme_f0(accent_phrases, speaker_id)

    def create_accent_phrases(self, text: str, speaker_id: int) -> List[AccentPhrase]:
        if len(text.strip()) == 0:
            return []

        utterance = extract_full_context_label(text)
        return self.replace_mora_pitch(
            accent_phrases=[
                AccentPhrase(
                    moras=[
                        Mora(
                            text=mora_to_text(
                                "".join([p.phoneme for p in mora.phonemes])
                            ),
                            consonant=(
                                mora.consonant.phoneme
                                if mora.consonant is not None
                                else None
                            ),
                            vowel=mora.vowel.phoneme,
                            pitch=0,
                        )
                        for mora in accent_phrase.moras
                    ],
                    accent=accent_phrase.accent,
                    pause_mora=(
                        Mora(text="、", consonant=None, vowel="pau", pitch=0)
                        if (
                                i_accent_phrase == len(breath_group.accent_phrases) - 1
                                and i_breath_group != len(utterance.breath_groups) - 1
                        )
                        else None
                    ),
                )
                for i_breath_group, breath_group in enumerate(utterance.breath_groups)
                for i_accent_phrase, accent_phrase in enumerate(
                    breath_group.accent_phrases
                )
            ],
            speaker_id=speaker_id,
        )

    async def synthesis(self, connection: ConnectionItem) -> None:
        speech_item = connection.speech_queue[0]
        text = ""
        if connection.name_speech:
            text = speech_item.username + "。"
        text += speech_item.content
        # 改行は句点として扱う
        text.replace("\n", "。")
        speaker_id = connection.speaker_id
        query = AudioQuery(
            accent_phrases=self.create_accent_phrases(text, speaker_id),
            speedScale=1,
            pitchScale=0,
            intonationScale=1,
            volumeScale=1,
        )

        wave = self.engine.synthesis(query, speaker_id)

        bytes_io = BytesIO()
        soundfile.write(file=bytes_io, data=wave, samplerate=24000, format="WAV")
        connection.voice_client.play(PCMVolumeTransformer(PCMAudio(bytes_io), volume=connection.volume / 100))

        while connection.voice_client.is_playing():
            await sleep(1)
        connection.speech_queue.pop(0)

        if speech_item.tts_end:
            guild_id: int = connection.voice_client.guild.id
            await connection.voice_client.disconnect()
            del self.connections[guild_id]
        elif len(connection.speech_queue) > 0:
            await self.synthesis(connection)

    async def text_to_speech(
            self,
            connection: ConnectionItem,
            content: str,
            username: str = "",
            tts_end: bool = False
    ) -> None:
        connection.speech_queue.append(SpeechQueueItem(content, username, tts_end))
        if not connection.voice_client.is_playing() or len(connection.speech_queue) == 1:
            await self.synthesis(connection)

    def create_db(self) -> None:
        create_tts_bot_table = """
            create table if not exists tts_bot(
                guild_id integer primary key,
                volume integer default 50,
                name_speech interger default 1
            )
        """
        self.cur.execute(create_tts_bot_table)
        self.con.commit()

    def get_volume(self, guild_id: int) -> Union[int, None]:
        sql = "select volume from tts_bot where guild_id = ?"
        self.cur.execute(sql, (guild_id,))
        result = self.cur.fetchone()
        if result is None:
            return None
        print(result)
        return result[0]

    def set_volume(self, guild_id: int, volume: int) -> None:
        # このUpsert構文はSQLite 3.24.1以降でなければ使えない。
        # Windowsに入るPython 3.7の標準SQLite Versionは3.21.0のため、使えない。
        # sql = """
        #     insert into tts_bot(guild_id, volume)
        #     values (?, ?)
        #     on conflict(guild_id)
        #     do update
        #     set volume=excluded.volume
        # """
        if self.get_volume(guild_id) is None:
            sql = """
                insert into tts_bot(volume, guild_id)
                values (?, ?)
            """
        else:
            sql = """
                update tts_bot set volume = ?
                where guild_id = ?
            """
        self.cur.execute(sql, (volume, guild_id))
        self.con.commit()
        connection = self.connections.get(guild_id)
        if connection:
            connection.volume = volume


    def get_name_speech(self, guild_id: int) -> Union[bool, None]:
        sql = "select name_speech from tts_bot where guild_id = ?"
        self.cur.execute(sql, (guild_id,))
        result = self.cur.fetchone()
        if result is None:
            return None
        return bool(result[0])

    def set_name_speech(self, guild_id: int, name_speech: bool) -> None:
        # sql = """
        #     insert into tts_bot(guild_id, name_speech)
        #     values (?, ?)
        #     on conflict(guild_id)
        #     do update
        #     set name_speech=excluded.name_speech
        # """
        if self.get_name_speech(guild_id) is None:
            sql = """
                insert into tts_bot(name_speech, guild_id)
                values (?, ?)
            """
        else:
            sql = """
                update tts_bot set name_speech = ?
                where guild_id = ?
            """
        self.cur.execute(sql, (int(name_speech), guild_id))
        self.con.commit()
        connection = self.connections.get(guild_id)
        if connection:
            connection.name_speech = name_speech


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_gpu", action="store_true")
    args = parser.parse_args()
    bot = TTSBotSample(command_prefix='?', use_gpu=args.use_gpu)
    bot.run(os.environ["TOKEN"])
