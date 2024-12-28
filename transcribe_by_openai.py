import os
import openai
import time

from dev_logger import logger


def get_openai_api_key():
    """
    OpenAI APIキーを取得

    :return: OpenAI APIキー
    """

    # Windows環境変数から取得
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        logger.error("OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。")
        raise Exception("OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。")  # 例外通知

    return openai_api_key


def export_audio_to_text_by_openai(audio_file_path, text_file_path):
    """
    openai を使って音声ファイルをテキストファイルに出力

    :param audio_file_path: 音声ファイルのパス
    :param output_audio_file_path: 出力テキストファイルのパス
    """

    logger.info(f"export_audio_to_text_by_openai() start -> {audio_file_path}")

    try:
        start_time = time.time()  # 開始時間の記録

        openai.api_key = get_openai_api_key()

        with open(audio_file_path, 'rb') as audio_file:
            # Whisper APIを呼び出して文字起こし
            transcript = openai.Audio.transcribe('whisper-1', audio_file)

            # テキストファイルに保存
            with open(text_file_path, 'w', encoding='utf-8') as f:
                f.write(transcript['text'])

            end_time = time.time()  # 終了時間の記録
            elapsed_time = end_time - start_time  # 経過時間

            logger.info(f"export_audio_to_text_by_openai() finish -> {text_file_path}, time:{elapsed_time:.2f} sec")
    
    except Exception as e:
        logger.error(f"export_audio_to_text_by_openai() failed -> {audio_file_path}: {e}")
        raise   # 例外通知


# OpenAI の使い方

# 1. アカウントの用意
# OpenAIアカウントを作成
# OpenAIのウェブサイト にアクセスします。
# https://platform.openai.com/docs/overview
# 「Sign up」をクリックし、メールアドレスやGoogleアカウントなどを用いてアカウントを作成します。
# アカウントを既に持っている場合は「Log in」からログインしてください。

# 2. アカウントへのログイン
# ログイン
# 成功裏にアカウントが作成されると、再びOpenAIプラットフォームへアクセスします。
# 「Log in」ボタンから登録したアカウント情報を用いてログインします。

# 3. APIキーの管理画面へ移動
# APIキー管理ページを開く
# ログイン後、右上に自分のアカウントアイコン（またはメールアドレス）が表示されます。それをクリックし、表示されるメニューから「View API keys」を選択します。
# 「View API keys」をクリックすると、APIキーの管理ページが表示されます。

# 4. APIキーの生成
# 新しいシークレットキー（Secret key）の発行
# 「Create new secret key」（新しいシークレットキーを作成）というボタンがあるはずです。これをクリックします。
# 数秒待つと、新しいAPIキーが表示されます。

# 5. APIキーの保管
# キーの保存
# ここで表示されたキーは一度だけ表示されます。後で再度表示させることはできません。
# 「Copy」ボタンを押してキーをコピーし、必ず安全な場所（パスワードマネージャーや安全なテキストファイルなど）に保存してください。
# 重要: このAPIキーを第三者に知られないよう注意してください。APIキーはあなた専用で、これが漏れると不正利用される危険があります。

# 6. Windows環境変数への設定方法
# Windowsでは、環境変数にAPIキーを設定することで、コード上にキーを直接記述せずに済むため、セキュリティや再利用性の観点からも有用です。
# 方法: システムのプロパティから設定
# 「環境変数」の設定画面を開く
# スタートメニューを開き、検索ボックスに「環境変数」と入力します。
# 検索結果から「システム環境変数の編集」を選択します。
# または、Windowsキー + Rで「ファイル名を指定して実行」を開き、sysdm.cplと入力してEnterを押し、「詳細設定」タブにある「環境変数」をクリックします。
# 環境変数の編集ウィンドウで新規変数を追加
# 「環境変数」ウィンドウが表示されたら、以下のいずれかを選択します。
# ユーザー環境変数: 現在のログインユーザーにのみ適用
# システム環境変数: このPCの全ユーザーに適用（管理者権限が必要）
# 「新規(N)...」ボタンをクリックします。
# 新しい環境変数の作成
# 「新しい○○変数」ダイアログが開くので、以下のように入力します。
# 変数名: OPENAI_API_KEY
# 変数値: 先ほど取得したAPIキー（sk-から始まるキー）
# 入力が終わったら「OK」をクリックします。
# 設定の反映
# 「環境変数」ウィンドウ、そして「システムのプロパティ」を「OK」で閉じます。
# 既に開いているコマンドプロンプトやPowerShellがあれば、再起動してください。新しい環境変数は、次回開いたターミナルやアプリケーションから有効になります。

# 7. 必要に応じた更新や削除
# キーのローテーション・削除
# 再度「View API keys」ページにアクセスすると、既に発行されたキーの一覧が表示されています（ただし値は表示されず、ラベルのみ）。
# 万が一キーが漏洩したと思われる場合は、そのキーを「Delete」ボタンで削除してください。
# 新しく必要な場合は再度「Create new secret key」から発行できます。
