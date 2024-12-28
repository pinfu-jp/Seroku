import os

from transcribe_mp3 import tanscribe_audio_file


if __name__ == '__main__':

    script_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_path = os.path.join(script_dir, 'tmp', 'input', 'test123.mp3')
    output_text_file = os.path.join(script_dir, 'tmp', 'output', 'output.txt')

    tanscribe_audio_file(mp3_path, output_text_file)
