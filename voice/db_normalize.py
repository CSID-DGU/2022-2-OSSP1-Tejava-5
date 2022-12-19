from voice import *

def db_normalize(input_file_name, de_identified_file_name):
    input_song = AudioSegment.from_wav(input_file_name)
    de_identified_song = AudioSegment.from_wav(de_identified_file_name)
    
    #evaluate dBFS difference between input_song and de_identified_song
    db_difference = input_song.dBFS - de_identified_song.dBFS
    
    #normalized dBFS
    normalized_song = de_identified_song + db_difference
    
    normalized_song.export("normalized_audio.wav", format='wav')
    os.remove(input_file_name)
    os.remove(de_identified_file_name)
    