# VOICEVOX ENGINE + Discord TTS Sample Bot

discord.pyを使ったDiscord Bot上に[VOICEVOX ENGINE](https://github.com/Hiroshiba/voicevox_engine)を用いたTTS機能を載せるサンプル。
Bot自体を製作者がホストして公開するのはライセンス的に微妙な気がするので、動作するコードを公開します。  
利用したい人がセルフホストして利用してください。  
また、本READMEはBot構築に関してある程度知識がある前提で書かれています。ご了承ください。

## 貢献者の方へ

Issue を解決するプルリクエストを作成される際は、別の方と同じ Issue に取り組むことを避けるため、
Issue 側で取り組み始めたことを伝えるか、最初に Draft プルリクエストを作成してください。

## 環境構築

### 必要なライブラリのインストール
```bash
# 開発に必要なライブラリのインストール
pip install -r requirements-test.txt

# とりあえず実行したいだけなら代わりにこちら
pip install -r requirements.txt
```

### Bot用Oauthトークンの取得と設定
まずはトークンをDiscord Developer Portalから取得してください。ここでは取得方法は省略します。
Git等に上げず、完全にローカル運用するのであれば、`run.py`の一番下にある以下の部分をトークンに書き換えていただいて構いません。
```diff
-bot.run(os.environ["TOKEN"])
+bot.run("<TOKEN>")
```
直接埋め込みたくない方は、`TOKEN`環境変数に設定しておく等、お好きな方法で設定してください。

## 実行

### 注意
- 本サンプルBotは現状、製品版 VOICEVOXがWindowsのみで公開されていることから、
  Windows以外では完全には動作しません。
- 製品版 VOICEVOXを利用するにあたり、Python 3.7以外を利用することができません。
```bash
# 製品版 VOICEVOXでBotを起動
# シェル変数はGit Bashなどでしか使えないため、その上で動かしてください。
VOICEVOX_DIR="C:/path/to/voicevox" # 製品版 VOICEVOX ディレクトリのパス
python run.py --voicevox_dir=$VOICEVOX_DIR
```

<!-- 差し替え可能な音声ライブラリまたはその仕様が公開されたらコメントを外す
```bash
# 音声ライブラリを差し替える
VOICELIB_DIR="C:/path/to/your/tts-model"
python run.py --voicevox_dir=$VOICEVOX_DIR --voicelib_dir=$VOICELIB_DIR
```
-->

```bash
# モックでBot起動(音声合成は行えません)
python run.py
```

## コードフォーマット

コードのフォーマットを整えます。プルリクエストを送る前に実行してください。

```bash
pysen run format lint
```

## ライセンス
本サンプルBotは[LGPLv3](LICENSE)で公開されています。
