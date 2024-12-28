import os
import tempfile
import shutil
from datetime import datetime

from dev_logger import logger
from split_audio import split_audio
from transcribe_by_openai import export_audio_to_text_by_openai


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


def process_audio_file(audio_file_path, text_file_path):
    """
    音声ファイルを文字起こしし、個別のテキストファイルに保存する。

    :param audio_file_path: 音声ファイルのパス
    :param text_file_path: 出力テキストファイルのパス
    """

    # OpenAI を使って音声ファイルをテキストファイルに出力
    export_audio_to_text_by_openai(audio_file_path, text_file_path)


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


