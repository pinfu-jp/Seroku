import logging
import os
from datetime import datetime

# logディレクトリパス
log_dir = os.path.join(os.getcwd(), "log")


class DevLogger:
    """
    開発用ログ
    """

    def __init__(self, log_level=logging.INFO):
        """
        DualLoggerクラスを初期化します。ログファイルとコンソールの両方に出力されるように設定します。
        
        Args:
            log_level (int): ログのレベル（例: logging.INFO）
        """
        # ログディレクトリの作成
        os.makedirs(log_dir, exist_ok=True)
        
        # ログファイルのパスを設定（タイムスタンプ付き）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"recorder_{timestamp}.log")
        
        # ロガーの設定
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # コンソール出力のハンドラ
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # ファイル出力のハンドラ
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        
        # フォーマットの設定
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # ハンドラをロガーに追加
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        """
        ロガーのインスタンスを取得します。
        
        Returns:
            logging.Logger: 設定済みのロガー
        """
        return self.logger


logger = DevLogger(log_level=logging.INFO).get_logger()
"""ロガー"""
