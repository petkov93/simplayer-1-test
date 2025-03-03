from vlc import State
from customtkinter import *
from tkinter import ttk
from PIL import Image
from mutagen.mp3 import MP3
from mediaplayer import Simplayer
import os


class MediaPlayerUI(CTk):
    def __init__(self, ):
        super().__init__()
        # variables
        self.sel_song_path = None
        self.selected_song = None
        self.song_index = None
        self.is_playing = False
        self.repeat_playlist = True
        self.current_volume = 0
        self.playlist = []
        # paths
        self.folder_path = os.path.join(os.path.join(os.path.expanduser('~'), 'Desktop'), 'YouTube')
        self.music_folder = os.listdir(self.folder_path)
        # images
        self.repeat_img = CTkImage(Image.open('./btnimgs/orange-repeat-circle.png'), size=(45, 45))
        self.repeat_1_img = CTkImage(Image.open('./btnimgs/orange-repeat-1-circle.png'), size=(45, 45))
        self.repeat_off_img = CTkImage(Image.open('./btnimgs/orange-repeat-off-circle.png'), size=(45, 45))
        self.shuffle_img = CTkImage(Image.open('./btnimgs/orange-shuffle.png'), size=(45, 45))

        self.prev_img = CTkImage(Image.open('./btnimgs/orange-prev.png'), size=(45, 45))
        self.play_img = CTkImage(Image.open('./btnimgs/orange-play.png'), size=(45, 45))
        self.pause_img = CTkImage(Image.open('./btnimgs/orange-pause.png'), size=(45, 45))
        self.next_img = CTkImage(Image.open('./btnimgs/orange-next.png'), size=(45, 45))
        self.stop_img = CTkImage(Image.open('./btnimgs/orange-stop.png'), size=(45, 45))

        self.mute_img = CTkImage(Image.open('./btnimgs/orange-mute.png'), size=(45, 45))
        self.vol_up_img = CTkImage(Image.open('./btnimgs/orange-volume-up.png'), size=(45, 45))
        self.vol_down_img = CTkImage(Image.open('./btnimgs/orange-volume-down.png'), size=(45, 45))
        # widgets init
        self.top_frame = CTkFrame(self, )
        self.progress_frame = CTkFrame(self, )
        self.btn_frame = CTkFrame(self, )
        self.playlist_frame = CTkFrame(self, )
        # progress bar
        self.progress_bar = CTkProgressBar(self.progress_frame, )
        self.volume_bar = CTkProgressBar(self.btn_frame, orientation='vertical')
        # playlist tree
        self.song_tree = ttk.Treeview(self.playlist_frame, )
        self.style = ttk.Style()
        # labels
        self.top_label = CTkLabel(self.top_frame, )
        self.repeat_label = CTkLabel(self.progress_frame, )
        self.time_left_label = CTkLabel(self.progress_frame, )
        # buttons
        self.repeat_btn = CTkButton(self.btn_frame, )
        self.shuffle_btn = CTkButton(self.btn_frame, )
        self.prev_btn = CTkButton(self.btn_frame, )
        self.play_btn = CTkButton(self.btn_frame, )
        self.next_btn = CTkButton(self.btn_frame, )
        self.stop_btn = CTkButton(self.btn_frame, )
        # volume ctrl buttons
        self.vol_mute_btn = CTkButton(self.btn_frame, )
        self.vol_up_btn = CTkButton(self.btn_frame, )
        self.vol_down_btn = CTkButton(self.btn_frame, )

        self.configure_window()
        self.player = Simplayer()
        self.setup_widgets()
        self.update_widgets()
        self.update_progress()
        self.autoplay()

        self.progress_bar.bind('<ButtonRelease-1>', self.seek_progress)
        self.song_tree.bind('<Double-1>', self.double_click_play)
        self.volume_bar.bind('<ButtonRelease-1>', self.seek_volume)

        self.mainloop()

    def configure_window(self):
        """ window set up """
        self.maxsize(width=480, height=800)
        self.title('SimPlæyer 1.0')
        self._set_appearance_mode('dark')

    def setup_widgets(self):
        self.setup_top_frame()
        self.setup_progress_bar()
        self.setup_button_frame()
        self.setup_playlist_frame()

    def setup_top_frame(self):
        self.top_label.configure(font=('Roboto', 16),
                                 text_color='gold',
                                 text='🎵  Welcome to my music app. 🎵 '
                                      '\n 🎵 SimPlæyer, v1.0 🎵 '
                                      '\n 🎵 Select a song to start the playback. 🎵',
                                 wraplength=350,
                                 height=80)
        self.top_frame.pack(padx=20, pady=(20, 5), fill='x')
        self.top_label.pack(padx=20, pady=10, fill='x')

    def setup_progress_bar(self):
        self.progress_frame.pack(padx=20, pady=5, fill='x', expand=True)

        self.progress_bar.configure(width=380, mode='determinate', progress_color='#ffbf00')
        self.progress_bar.set(0)
        self.time_left_label.configure(text='00:00/00:00', )
        self.repeat_label.configure(text='Repeat: All', )

        self.progress_bar.grid(column=0, row=0, columnspan=2, padx=20, pady=10, sticky='ew')
        self.repeat_label.grid(column=0, row=1, padx=25, pady=5, sticky='sw')
        self.time_left_label.grid(column=1, row=1, padx=25, pady=5, sticky='es')

    def update_progress(self):
        self.progress_bar.set(self.player.progress)
        self.time_left_label.configure(text=self.player.time_left_str)
        self.after(1000, self.update_progress)

    def seek_progress(self, event):
        length = self.player.mediaPlayer.get_length() / 1000  # time in sec
        click_pos = event.x / self.progress_bar.winfo_width()
        new_time = int(length * click_pos * 1000)  # converts back to ms
        self.player.mediaPlayer.set_time(new_time)

    def seek_volume(self, event):
        self.current_volume = (1 - (event.y / self.volume_bar.winfo_height())) * 100
        if self.current_volume > 100:
            self.current_volume = 100
        if self.current_volume < 0:
            self.current_volume = 0
        self.player.set_volume(self.current_volume)
        self.volume_bar.set(self.current_volume / 100)
        # print('mouse click : ', self.player.mediaPlayer.audio_get_volume())

    def setup_button_frame(self):
        self.btn_frame.pack(
            padx=20,
            pady=5,
            fill='both')

        def configure_buttons():
            # repeat button
            self.repeat_btn.configure(
                text='',
                command=self.repeat_btn_clicked,
                image=self.repeat_img,
                fg_color='gray17',
                hover_color='gray23',
                border_spacing=0,
                width=30,
                height=30, )
            self.prev_btn.configure(
                text='',
                command=self.prev_btn_clicked,
                image=self.prev_img,
                fg_color='gray17',
                hover_color='gray23',
                border_spacing=0,
                width=30,
                height=30)
            self.play_btn.configure(
                text='',
                command=self.play_btn_clicked,
                image=self.play_img,
                fg_color='gray17',
                hover_color='gray23',
                border_spacing=0,
                width=30,
                height=30)
            self.next_btn.configure(
                text='',
                command=self.next_btn_clicked,
                image=self.next_img,
                fg_color='gray17',
                hover_color='gray23',
                border_spacing=0,
                width=30,
                height=30)
            self.stop_btn.configure(
                text='',
                command=self.stop_btn_clicked,
                image=self.stop_img,
                fg_color='gray17',
                hover_color='gray23',
                border_spacing=0,
                width=30,
                height=30)
            self.shuffle_btn.configure(
                fg_color='gray17',
                text='',
                hover_color='gray23',
                width=30,
                height=30,
                image=self.shuffle_img)
            self.vol_mute_btn.configure(
                width=30,
                height=30,
                text='',
                image=self.mute_img,
                fg_color='gray17',
                hover_color='gray23',
                command=self.vol_mute)
            self.vol_up_btn.configure(
                text='',
                width=30,
                height=30,
                image=self.vol_up_img,
                fg_color='gray17',
                hover_color='gray23',
                command=self.vol_up)
            self.vol_down_btn.configure(
                text='',
                width=30,
                height=30,
                image=self.vol_down_img,
                fg_color='gray17',
                hover_color='gray23',
                command=self.vol_down)

        def place_buttons():
            self.repeat_btn.grid(column=0, row=0, padx=2, pady=2,)
            self.prev_btn.grid(column=1, row=0, padx=2, pady=2, )
            self.play_btn.grid(column=2, row=0, padx=2, pady=2)
            self.next_btn.grid(column=3, row=0, padx=2, pady=2)
            self.stop_btn.grid(column=4, row=0, padx=2, pady=2)
            self.shuffle_btn.grid(column=0, row=1, pady=2, padx=2, )
            self.vol_mute_btn.grid(column=4, row=1, pady=2, padx=2, )
            self.vol_down_btn.grid(column=5, row=1, padx=2, pady=2, )
            self.vol_up_btn.grid(column=5, row=0, padx=2, pady=2, )

        def configure_vol_bar():
            self.volume_bar.configure(height=100, width=8, progress_color='gold', mode='determinate')
            self.volume_bar.grid(column=6, row=0, rowspan=2, padx=(8, 10), pady=5)
            self.current_volume = self.player.mediaPlayer.audio_get_volume()
            self.volume_bar.set(self.current_volume / 100)

        configure_buttons()
        place_buttons()
        configure_vol_bar()

    def vol_up(self):
        if self.current_volume > 99:
            return
        else:
            self.current_volume += 5
            self.player.set_volume(self.current_volume)
            self.volume_bar.set(self.current_volume / 100)

            print('vol + :', self.player.mediaPlayer.audio_get_volume())

    def vol_down(self):
        if self.current_volume < 5:
            return
        else:
            self.current_volume -= 5
            self.player.set_volume(self.current_volume)
            self.volume_bar.set(self.current_volume / 100)

            print('vol - :', self.player.mediaPlayer.audio_get_volume())

    def vol_mute(self):
        self.current_volume = 0
        self.player.set_volume(self.current_volume)
        self.volume_bar.set(self.current_volume)

    def setup_playlist_frame(self):
        def get_treeview_id_by_song_name(song_name):
            """Find the Treeview item ID that corresponds to a given song name."""
            for item in self.song_tree.get_children():
                song_title = self.song_tree.item(item, "values")[0].strip()  # Get the song name from the first column
                if song_title == song_name:
                    return item  # Return the item ID
            return None  # Return None if not found

        def highlight_playing():
            if self.player.mediaPlayer.get_state() in [State.Playing, State.Paused]:
                for item in self.song_tree.get_children():
                    self.song_tree.item(item, tags=('normal', ))
                song_id = get_treeview_id_by_song_name(self.selected_song)
                if song_id:
                    self.song_tree.item(song_id, tags=('playing', ))

            self.after(200, highlight_playing)

        self.style.configure("Treeview",  # Custom style name
                             font=('Aerial', 12, 'bold'),
                             background="gray13",  # Background color for rows
                             fieldbackground="gray10",  # Background color for the widget
                             foreground="#b38600")  # Text color
        self.style.map("Custom.Treeview",
                       background=[('selected', '#b38600')],
                       foreground=[('selected', 'gray13')])  # Selected row color
        self.song_tree.tag_configure("normal",
                                     background="gray13",
                                     foreground="#b38600")  # Default color
        self.song_tree.tag_configure("playing",
                                     background="gray25",
                                     foreground="gold")  # Playing row
        self.song_tree.configure(
                                style='Treeview',
                                selectmode='browse',
                                columns=('Song name', 'Length'))

        self.playlist_frame.pack(padx=20,
                                 pady=(10, 20),
                                 fill='x', )
        self.song_tree.heading('#0', text='N', anchor='center')
        self.song_tree.heading('#1', text='Song name', anchor='w')
        self.song_tree.heading('#2', text='Length', anchor='s')
        self.song_tree.column('#0', minwidth=10, width=10)
        self.song_tree.column(column='#1', width=320)
        self.song_tree.column(column='#2', width=30, anchor='e')
        self.song_tree.pack(fill='x', expand=False)

        self.load_playlist()
        highlight_playing()

    def load_playlist(self):
        # fetches the songs from the YouTube folder
        for i in self.music_folder:
            if i.endswith('.mp3'):
                self.playlist.append(i)
        # fetches the songs to the playlist
        for index, item in enumerate(self.playlist):
            file_len = MP3(os.path.join(self.folder_path + '/' + item))
            mins = int(file_len.info.length // 60)
            secs = int(file_len.info.length % 60)
            length = f'{mins}:{secs:02}'
            self.song_tree.insert(
                '',
                index="end",
                text=f'{index + 1}',
                values=(f' {item}', f'{length}'))

    def get_selected_song(self):
        """ Sets the selected song  as self.selected_song / self.sel_song_path """
        song_id = self.song_tree.focus()  # returns id of selected song
        if not song_id:
            self.top_label.configure(text='Cant play. Nothing selected..')
            return
        song_data = self.song_tree.item(song_id).get('values')
        if not song_data or len(song_data) < 1:
            self.top_label.configure(text='Invalid song')
            return
        self.selected_song = song_data[0].strip()
        self.sel_song_path = os.path.join(self.folder_path, self.selected_song)

    def play_song(self, index=0):
        if self.song_index is None or not self.selected_song:
            self.get_selected_song()
            if not self.selected_song:
                self.top_label.configure(text='No song selected from the playlist!')
        self.song_index = (self.playlist.index(self.selected_song) + index) % len(self.playlist)
        self.selected_song = self.playlist[self.song_index]
        self.sel_song_path = os.path.join(self.folder_path, self.selected_song)
        self.player.play(self.sel_song_path)

    def update_widgets(self):
        if self.player.mediaPlayer.get_state() == State.Playing:
            self.play_btn.configure(image=self.pause_img)
            self.top_label.configure(text=f'Now playing:\n\n🎶 {self.selected_song} 🎶')
        elif self.player.mediaPlayer.get_state() == State.Paused:
            self.play_btn.configure(image=self.play_img)
            self.top_label.configure(text=f'Paused: \n\n🎶 {self.selected_song} 🎶')
        elif self.player.mediaPlayer.get_state() == State.Stopped:
            self.play_btn.configure(image=self.play_img)
            self.top_label.configure(text='Playback stopped.\n\n -❌-')
        elif self.player.mediaPlayer.get_state() == State.NothingSpecial:
            self.play_btn.configure(image=self.play_img)

        self.after(200, self.update_widgets)

    def double_click_play(self, event):
        self.song_index = None
        self.selected_song = None
        self.get_selected_song()
        self.play_song(0)

    def autoplay(self):
        if self.repeat_playlist is True:
            if self.player.mediaPlayer.get_state() == State.Ended:
                self.play_song(1)
            self.after(500, self.autoplay)

    def play_btn_clicked(self, ):
        # play new song
        if self.player.mediaPlayer.get_state() in [State.Stopped, State.Ended, State.NothingSpecial]:
            self.play_song(0)
        # if the player is playing -> pause()
        elif self.player.mediaPlayer.get_state() == State.Playing:
            self.player.pause()
        # if the player is paused -> resume playing()
        elif self.player.mediaPlayer.get_state() == State.Paused:
            self.player.resume_playing()

    def stop_btn_clicked(self):
        self.player.stop_playing()
        self.selected_song = None
        self.song_index = None
        self.progress_bar.set(0)

    def prev_btn_clicked(self):
        if self.song_index is None or not self.selected_song:
            self.get_selected_song()
            self.song_index = self.playlist.index(self.selected_song)
        self.play_song(-1)

    def next_btn_clicked(self):
        if self.song_index is None or not self.selected_song:
            self.get_selected_song()
            self.song_index = self.playlist.index(self.selected_song)
        self.play_song(1)

    def repeat_btn_clicked(self):
        if self.repeat_playlist is True:
            self.repeat_playlist = False
            self.repeat_label.configure(text='Repeat: Off')
        elif self.repeat_playlist is False:
            self.repeat_playlist = True
            self.repeat_label.configure(text='Repeat: All')


if __name__ == '__main__':
    app = MediaPlayerUI()
