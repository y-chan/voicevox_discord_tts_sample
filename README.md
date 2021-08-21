# VOICEVOX ENGINE + Discord TTS Sample Bot

discord.pyを使ったDiscord Bot上に[VOICEVOX ENGINE](https://github.com/Hiroshiba/voicevox_engine)を用いたTTS機能を載せるサンプル。
Bot自体を製作者がホストして公開するのはライセンス的に微妙な気がするので、動作するコードを公開します。  
利用したい人がセルフホストして利用してください。  
また、本READMEはBot構築に関してある程度知識がある前提で書かれています。ご了承ください。

## 環境構築

### 必要なライブラリのインストール
```bash
pip install -r requirements.txt -r requirements-dev.txt
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
CODE_DIRECTORY=$(pwd) # コードがあるディレクトリのパス
cd $VOICEVOX_DIR
PYTHONPATH=$VOICEVOX_DIR python $CODE_DIRECTORY/run.py
```

```bash
# モックでBot起動(音声合成は行えません)
python run.py
```

## ライセンス
本サンプルBotは[LGPLv3](LICENSE)で公開されています。
