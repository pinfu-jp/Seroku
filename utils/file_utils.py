import os
import shutil
import sys
import subprocess

def open_with_default_app(file_path):
    """
    引数で与えたファイルをOSの既定アプリで開く関数
    :param file_path: 開きたいファイルのパス
    """
    # OSの種類を判定し、それぞれ対応する方法でファイルを開く
    if sys.platform.startswith('win'):  
        # Windowsの場合は os.startfile を使う
        os.startfile(file_path)
    elif sys.platform.startswith('darwin'):
        # macOSの場合は subprocess で「open」コマンドを呼び出す
        subprocess.run(["open", file_path])
    else:
        # Linuxの場合は subprocess で「xdg-open」コマンドを呼び出す
        subprocess.run(["xdg-open", file_path])