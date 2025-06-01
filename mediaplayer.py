import threading
from vlc import MediaPlayer, Media, State
from time import sleep


class Simplayer:
    def __init__(self):
        self.main_thread = None
        # file_path = r'C:\Users\petko\My Files\Udemy\Python 100 Day challenge\PyCharm projects\CustomTkinter1\2Pac - Changes ft. Talent.mp3'
        # self.song_path = file_path
        self.media = None
        self.mediaPlayer = MediaPlayer()
        self.mediaPlayer.audio_set_volume(50)
        self.time_left_str = '00:00/00:00'
        self.progress = 0

    def play(self, song):
        def play_new_song():
            self.media = Media(song)
            self.mediaPlayer.set_media(self.media)
            self.mediaPlayer.play()
            sleep(1)
            self.get_progress()

        self.main_thread = threading.Thread(target=play_new_song, daemon=True).start()

    def pause(self):
        self.mediaPlayer.set_pause(do_pause=True)

    def resume_playing(self):
        self.mediaPlayer.set_pause(do_pause=False)

    def stop_playing(self):
        self.mediaPlayer.stop()

    def get_progress(self):
        def ms_to_min_sec(ms):
            mins = int(ms // 60)
            secs = int(ms % 60)
            return f'{mins}:{secs:02}'

        while self.mediaPlayer.get_state() in [State.Playing, State.Paused]:
            total_duration = self.mediaPlayer.get_length() / 1000  # in seconds
            current_time = self.mediaPlayer.get_time() / 1000  # in seconds
            if total_duration > 0:
                self.progress = (current_time / total_duration)
                self.time_left_str = f'{ms_to_min_sec(current_time)}/{ms_to_min_sec(total_duration)}'
                sleep(0.1)

    def set_volume(self, volume):
        self.mediaPlayer.audio_set_volume(int(volume))
