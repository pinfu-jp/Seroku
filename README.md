
正しい仮想環境が有効化されているか確認

VSCodeで使用している仮想環境が正しいか確認します。VSCodeで異なる環境を使用していると、Pylanceがパッケージを見つけられない場合があります。

VSCodeのコマンドパレットを開く：Ctrl+Shift+P を押して、コマンドパレットを開きます。
"Python: Select Interpreter" を選択：現在のプロジェクトの仮想環境（venvなど）を選択します。
選択後、VSCodeのターミナルにpythonと入力して、インタープリタが選択した仮想環境になっていることを確認してください。

python 仮想環境を有効化

ターミナル（pwsh）で以下を実行する
```
.\venv\Scripts\activate
```

新しい環境でライブラリを取得する場合は、ターミナルで以下のコマンドを実行すること

```
pip install -r requirements.txt
```

