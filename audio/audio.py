# audio.py - CS3100 - Myles Hammerschmidt
# -This file initializes the pygame mixer object and loads all audio assets.
# -Note: Mixer must be initialized here in order to load audio files.
from pygame import mixer
from pkg_resources import resource_filename
bgm_path = resource_filename('audio', 'bgm')
sfx_path = resource_filename('audio', 'sfx')

#Initialize mixer with pre_init values. (Helps with latency)
mixer.pre_init(44100, -16, 2, 1024)
mixer.init()

#Load SFX
sfx_card_draw = mixer.Sound(sfx_path + '/Card_Draw.wav')
sfx_card_place = mixer.Sound(sfx_path + '/Card_Place.wav')
sfx_card_shuffle = mixer.Sound(sfx_path + '/Card_Shuffle.wav')
sfx_ding = mixer.Sound(sfx_path + '/Ding.wav')
sfx_error = mixer.Sound(sfx_path + '/Error.wav')
sfx_uno = mixer.Sound(sfx_path + '/Uno.wav')

#Load First Song
mixer.music.load(bgm_path + '/Lobby_Music.mp3')
mixer.music.set_volume(0.65)