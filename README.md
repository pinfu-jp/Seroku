# 音録（Seroku）とは

- 音声データをテキストに文字お越しするプログラムです
- Windows11 で動作確認しています
- OpenAI の API を使っています
  - API の仕様に合わせるために、音声データをいったん20MB単位に分割して文字お越しします
  - 文字お越し後、テキストファイルを統合して１つのテキストファイルにして出力します
- 中間ファイルは %TEMP%\transcribe_mp3\ に一時保存されます 

<br>

# 利用準備

- APIを使うために OpenAIプラットフォーム でライセンス契約が必要です
  - https://platform.openai.com/docs/overview

- OpenAIプラットフォーム で 新しい APIキー を生成して秘密鍵を作成します

- 秘密鍵を、自分の Windows マシンの環境変数に登録します
  - 変数名: OPENAI_API_KEY
  - 変数値: 先ほど取得したAPIキー（sk-から始まるキー）

<br>

# 実行方法

インターネットに接続された環境で、以下の手順で実行します。

1. mp3形式の音声ファイルを <プロジェクト>/tmp/input フォルダにコピー
2. main.py を実行
3. しばらくすると、<プロジェクト>/tmp/output フォルダに、output.txt ファイルが出力される

## API 利用料金の目安

- 40分程度の音声で、0.2ドル程度でした（2024.11時点）

<br>

# 開発環境構築方法

## VSCode のインストール

- Python 拡張機能のインストール

## GitHubからクローン

- URL はこちら
```
https://github.com/pinfu-jp/Seroku
```

## python 仮想環境を有効化

VSCodeのコマンドパレットを開く：Ctrl+Shift+P を押して、コマンドパレットを開きます。
"Python: Select Interpreter" を選択：現在のプロジェクトの仮想環境（venvなど）を選択します。
選択後、VSCodeのターミナルにpythonと入力して、インタープリタが選択した仮想環境になっていることを確認してください。

ターミナル（pwsh）で以下を実行する
```
.\venv\Scripts\activate
```

## python ライブラリのインストール

ターミナルで以下のコマンドを実行

```
pip install -r requirements.txt
```

以上