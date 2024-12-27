
# 音録（Seroku）とは

- 音声データをテキストに文字お越しするプログラムです
- OpenAI の API を使っています


# 利用準備

- APIを使うために OpenAIプラットフォーム でライセンス契約が必要です
  - https://platform.openai.com/docs/overview

- OpenAIプラットフォーム で 新しい APIキー を生成して秘密鍵を作成します

- 秘密鍵を、自分の Windows マシンの環境変数に登録します
  - 変数名: OPENAI_API_KEY
  - 変数値: 先ほど取得したAPIキー（sk-から始まるキー）
  

# 開発環境構築方法

## VSCode のインストール

### Python 拡張機能のインストール

## GitHubからクローン

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