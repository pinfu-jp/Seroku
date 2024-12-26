import os
import subprocess
from pydub import AudioSegment

BYTES_IN_MB = 1024 * 1024 * 8

def split_audio(input_file, output_folder='output_chunks', max_size_mb=20, bitrate='192k', 
                silence_thresh=-35, min_silence_len=3000, silence_padding=500):
    # 日本語コメント：
    # silence_threshをより小さくする（例：-35dBにする）ことで、より静かな箇所のみ無音と判断
    # min_silence_lenを3秒(3000ms)にすることで、短い切れ目でのカットを防止
    # silence_paddingは、検出した無音境界から前後に500ms程度ずらして、より自然な分割点にする
    
    # 入力ファイル検証
    if not validate_file(input_file):
        return
    
    # 出力フォルダの作成
    os.makedirs(output_folder, exist_ok=True)
    
    # WAV変換
    wav_file = convert_to_wav(input_file)
    
    # ffmpegでの無音検出
    silence_ranges = ffmpeg_detect_silence(wav_file, silence_thresh, min_silence_len)
    
    # 無音区間にパディングを追加（境界を少しずらす）
    adjusted_silence_ranges = []
    for start_ms, end_ms in silence_ranges:
        # 日本語コメント：無音範囲を少し拡大または縮小して、チャンク切り方を自然にする
        adjusted_start = max(0, start_ms - silence_padding)
        adjusted_end = end_ms + silence_padding
        adjusted_silence_ranges.append((adjusted_start, adjusted_end))
    
    # 音声ロード
    audio = AudioSegment.from_file(wav_file)
    
    # 最大許容長(ms)計算
    max_duration_ms = calculate_max_duration(max_size_mb, bitrate)
    
    # チャンク出力
    export_audio_chunks(audio, adjusted_silence_ranges, max_duration_ms, output_folder, input_file, bitrate)
    
    # 一時ファイル削除
    if os.path.exists(wav_file):
        os.remove(wav_file)

def validate_file(input_file):
    # 日本語コメント：ファイル存在＆MP3形式チェック
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"エラー: ファイルが見つかりません -> {input_file}")
    if not input_file.lower().endswith('.mp3'):
        raise ValueError(f"エラー: 入力ファイルはMP3形式である必要があります -> {input_file}")
    return True

def convert_to_wav(input_file):
    # 日本語コメント：MP3をWAVに変換
    wav_file = os.path.splitext(input_file)[0] + ".wav"
    audio = AudioSegment.from_file(input_file)
    audio.export(wav_file, format="wav")
    return wav_file

def ffmpeg_detect_silence(wav_file, silence_thresh, min_silence_len):
    # 日本語コメント：
    # ffmpegのsilencedetectフィルタを使い、dB閾値と無音時間を調整する
    # ここでは閾値を例：noise=-35dB、d=3.0sなど
    silence_db = silence_thresh
    silence_sec = min_silence_len / 1000.0
    
    cmd = [
        "ffmpeg",
        "-i", wav_file,
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
    
    return silence_ranges

def calculate_max_duration(max_size_mb, bitrate):
    # 日本語コメント：
    # MBとbitrateから最大許容長(ms)算出
    bitrate_kbps = int(bitrate.replace('k', ''))
    max_duration_sec = (max_size_mb * BYTES_IN_MB) / (bitrate_kbps * 1000)
    return max_duration_sec * 1000  # msへ変換

def export_audio_chunks(audio, silence_ranges, max_duration_ms, output_folder, input_file, bitrate):
    # 日本語コメント：
    # 無音区間のリストに基づきチャンクを切り出す
    
    if not silence_ranges:
        print("警告: 無音区間が検出されなかったため、音声全体を1つのチャンクとして保存します。")
        save_chunk(audio, output_folder, os.path.splitext(os.path.basename(input_file))[0], 1, bitrate)
        return
    
    start_time = 0
    chunk_index = 1
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    for silence_start, silence_end in silence_ranges:
        # チャンクの長さがmax_duration_msを超えそうな場合、ここでカット
        if (silence_start - start_time) >= max_duration_ms:
            if start_time >= len(audio) or silence_start > len(audio):
                print("警告: 範囲外インデックスが発生。処理を中断します。")
                break
            save_chunk(audio[start_time:silence_start], output_folder, base_name, chunk_index, bitrate)
            chunk_index += 1
            start_time = silence_start
    
    # 最後のチャンクを保存
    if start_time < len(audio):
        save_chunk(audio[start_time:], output_folder, base_name, chunk_index, bitrate)

def save_chunk(chunk, output_folder, base_name, chunk_index, bitrate):
    # 日本語コメント：チャンクをMP3で出力
    output_file = os.path.join(output_folder, f"{base_name}_{chunk_index}.mp3")
    try:
        chunk.export(output_file, format="mp3", bitrate=bitrate)
        print(f"チャンク{chunk_index}を保存しました: {output_file}")
    except Exception as e:
        print(f"エラー: チャンク{chunk_index}の保存に失敗しました -> {e}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'tmp', 'input', 'test123.mp3')
    output_folder = os.path.join(script_dir, 'tmp', 'output')
    
    # パラメータを調整：より長くて静かな無音のみ区切りとする
    split_audio(
        input_file, 
        output_folder, 
        max_size_mb=20, 
        bitrate='192k', 
        silence_thresh=-35,      # より低いdBを設定し、本当に静かなところのみ分割点とする
        min_silence_len=3000,    # 3秒以上の無音でようやく分割
        silence_padding=500      # 無音区間前後に500ms余裕を持たせる
    )
