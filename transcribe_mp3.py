import os
import openai
import tempfile
import shutil
from datetime import datetime

from split_audio import split_audio
from dev_logger import logger


def tanscribe_audio_file(mp3_path, out_text_path):
    """
    指定された音声ファイルを文字起こしし、結果をテキストファイルに保存します。

    :param mp3_path: 音声ファイルのパス
    :param out_text_path: 出力先のテキストファイルのパス
    """

    logger.info(f"start mp3_path:{mp3_path} out_text_path:{out_text_path}")

    tmp_dir_path = create_tmp_dir()

    # 解析可能なサイズへ音声ファイルを分割
    split_audio(mp3_path, tmp_dir_path)

    # 音声ファイル群を解析
    transcribe_audio_files(tmp_dir_path, out_text_path)

    # 後処理：テンポラリ削除
    if os.path.exists(out_text_path):
        delete_directory(tmp_dir_path)


def create_tmp_dir():
    """
    テンポラリに作業フォルダを作成
    %TEMP%\<pyファイル名>\<タイムスタンプ>
    """

    # テンポラリディレクトリを取得
    temp_dir = tempfile.gettempdir()

    # スクリプト名称(拡張子なし)
    script_name = os.path.splitext(os.path.basename(__file__))[0]

    # サブフォルダとしてタイムスタンプ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 例: "20241208_145210"
    tmp_path = os.path.join(temp_dir, script_name, timestamp)

    # フォルダのネスト作成（存在しない場合のみ作成）
    logger.info(f"makedirs path:{tmp_path}")
    os.makedirs(tmp_path, exist_ok=True)

    return tmp_path


def transcribe_audio_files(mp3_folder, output_text_file):
    """
    指定されたフォルダ内の音声ファイルを文字起こしし、個別のテキストファイルに保存。
    さらに、全結果を一つのテキストファイルに結合して保存します。

    :param mp3_folder: 音声ファイルが保存されているフォルダのパス（ファイル名昇順で処理）
    :param output_text_file: 出力先の結合テキストファイルのパス
    """
    # OpenAI APIキーの設定
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        logger.error("OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。")
        return

    openai.api_key = openai_api_key

    # フォルダ内のファイルを取得し、ソート（順番に処理するため）
    file_list = sorted(os.listdir(mp3_folder))

    # 個別テキストファイルを保存するための一時ディレクトリを作成
    temp_output_dir = os.path.join(mp3_folder, "temp_transcripts")
    os.makedirs(temp_output_dir, exist_ok=True)

    # 出力ファイルを追記モードで開く
    try:
        with open(output_text_file, 'w', encoding='utf-8') as output_file:
            for file_name in file_list:
                file_path = os.path.join(mp3_folder, file_name)

                # 音声ファイルでない場合はスキップ
                if not is_audio_file(file_name):
                    logger.info(f"スキップ: 音声ファイルではありません -> {file_name}")
                    continue

                # 個別テキストファイルのパス
                transcript_file_path = os.path.join(temp_output_dir, f"{os.path.splitext(file_name)[0]}.txt")

                # 音声ファイルを処理
                process_audio_file(file_path, transcript_file_path)
                try:
                    with open(transcript_file_path, 'r', encoding='utf-8') as f:
                        transcript_text = f.read()
                        # 結合ファイルに追記
                        output_file.write(transcript_text + '\n')
                except Exception as e:
                    logger.error(f"個別テキストファイルの読み込み失敗 -> {transcript_file_path}: {e}")

        logger.info(f"文字起こし結果を保存 -> {output_text_file}")
    except Exception as e:
        logger.error(f"結合テキストファイルへの保存失敗 -> {output_text_file}: {e}")


def is_audio_file(file_name):
    """
    ファイル名が音声ファイルであるかを判定する。
    """
    audio_extensions = ('.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac')
    return file_name.lower().endswith(audio_extensions)


def process_audio_file(file_path, output_file_path):
    """
    音声ファイルを文字起こしし、個別のテキストファイルに保存する。

    :param file_path: 音声ファイルのパス
    :param output_file_path: 出力テキストファイルのパス
    """

    file_name = os.path.splitext(os.path.basename(file_path))[0]

    logger.info(f"文字起こし開始 -> {file_path}")
    try:
        with open(file_path, 'rb') as audio_file:
            # Whisper APIを呼び出して文字起こし
            transcript = openai.Audio.transcribe('whisper-1', audio_file)

            # テキストファイルに保存
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(transcript['text'])

            logger.info(f"文字起こし完了 -> {output_file_path}")
    except Exception as e:
        logger.error(f"文字起こし失敗 -> {file_path}: {e}")
        raise   # 例外通知

def delete_directory(directory):
    """
    指定されたディレクトリを削除します。

    :param directory: 削除するディレクトリのパス
    """
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"ディレクトリを削除しました: {directory}")
        else:
            print(f"警告: 指定されたディレクトリは存在しません -> {directory}")
    except Exception as e:
        print(f"エラー: ディレクトリの削除に失敗しました -> {e}")


if __name__ == '__main__':

    script_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_path = os.path.join(script_dir, 'tmp', 'input', 'test123.mp3')
    # mp3_folder = os.path.join(script_dir, 'tmp', 'output')
    output_text_file = os.path.join(script_dir, 'tmp', 'output', 'output.txt')

    # transcribe_audio_files(mp3_folder, output_text_file)
    tanscribe_audio_file(mp3_path, output_text_file)


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
