import subprocess
import time

from utils.dev_logger import logger

# ffmpeg 関連機能

def detect_silence_by_ffmpeg(wav_file_path, silence_thresh, min_silence_len):
    """
    ffmpegを使って音声ファイルから無音区間を検出します。

    :param wav_file_path: WAVファイルのパス
    :param silence_thresh: 無音と判断するdB閾値
    :param min_silence_len: 無音と判断する最小長さ
    :return: 無音区間のリスト
    """

    logger.info(f"detect_silence_by_ffmpeg() start wav_path:{wav_file_path}")

    start_time = time.time()  # 開始時間の記録

    # ffmpegのsilencedetectフィルタを使い、dB閾値と無音時間を調整する
    # ここでは閾値を例：noise=-35dB、d=3.0sなど
    silence_db = silence_thresh
    silence_sec = min_silence_len / 1000.0
    
    cmd = [
        "ffmpeg",
        "-i", wav_file_path,
        "-af", f"silencedetect=noise={silence_db}dB:d={silence_sec}",
        "-f", "null",
        "-"
    ]
    
    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    lines = result.stderr.split('\n')
    
    silence_ranges = []
    current_start = None
    
    for line in lines:
        if "silence_start:" in line:
            parts = line.strip().split("silence_start: ")
            if len(parts) > 1:
                current_start = float(parts[1])
        elif "silence_end:" in line:
            parts = line.strip().split("silence_end: ")
            if len(parts) > 1 and current_start is not None:
                end_str = parts[1].split('|')[0].strip()
                silence_end = float(end_str)
                silence_ranges.append((int(current_start * 1000), int(silence_end * 1000)))
                current_start = None

    end_time = time.time()  # 終了時間の記録
    elapsed_time = end_time - start_time  # 経過時間

    logger.info(f"detect_silence_by_ffmpeg() end time:{elapsed_time:.2f} sec")

    return silence_ranges


# 1. ffmpeg のダウンロード
# ブラウザで以下のURLにアクセス

# https://github.com/BtbN/FFmpeg-Builds/releases
# ここでは、Windows向けのビルド済みファイル（.zip）が配布されています。
# ページを下にスクロールして、任意のアーカイブをダウンロード

# たとえば「ffmpeg-master-latest-win64-gpl-shared.zip」など。
# 「shared」と「static」でビルドが異なりますが、通常は「shared」版で問題ありません。
# GPU支援などの有無（gpl, lgpl）など細かな違いがありますが、ひとまず初回は「gpl」「master-latest」を選べばOKです。
# zipファイルを任意のフォルダに保存

# 例：C:\Users\ユーザー名\Downloads など。

# 2. ffmpeg の解凍と配置
# ダウンロードしたzipファイルを解凍

# 解凍すると「ffmpeg-master-latest-win64-gpl-shared」などのフォルダが展開されます。
# わかりやすい場所にフォルダを移動

# 例：C:\Program Files\ffmpeg など、後から思い出しやすいフォルダに配置するのがおすすめです。
# 解凍したフォルダ名が長い場合は、適宜リネームしても大丈夫です。（例：C:\Program Files\ffmpeg\）

# 3. 環境変数にパスを追加（Windows 10/11 の場合）
# 「システムのプロパティ」を開く

# Windowsキーを押して「環境変数」と入力すると、「システム環境変数の編集」という項目が出てきます。これをクリック。
# または 「Windowsの設定」→「システム」→「バージョン情報」→ 右ペインの「システムの詳細設定」でもOKです。
# 「システムのプロパティ」ウィンドウが開いたら、下部の「環境変数(N)...」をクリック

# 「システム環境変数」欄の中から、Path を探し、選択して「編集」をクリック

# ※ユーザー環境変数ではなくシステム環境変数の方に追加するほうが、PC全体で使いやすいです。
# （ユーザー単位で使うならユーザー環境変数のPathに追加しても良いです）
# 「環境変数の編集」画面で「新規(N)」をクリックし、解凍したffmpegの「bin」フォルダのパスを入力

# 例：C:\Program Files\ffmpeg\bin
# binフォルダ内に ffmpeg.exe, ffprobe.exe など実行ファイルが含まれています。
# 「OK」をクリックしてすべてのダイアログを閉じる

# 4. 動作確認
# 新規のコマンドプロンプトやPowerShellを開く

# 既に開いているコマンドプロンプトには、変更した環境変数が反映されていないので注意。
# 以下のコマンドを入力し、バージョン情報が出ればOK

# bash
# コードをコピーする
# ffmpeg -version
# バージョン番号やコンパイル情報が表示されれば、正常にインストールされています。

