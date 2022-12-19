from voice import *

def wav_to_mp3(de_identified_wav):
    #files
    wav_file = de_identified_wav
    mp3_file = "de_identified_audio.mp3"
    
    #convert mp3 file to wav file
    audSeg = AudioSegment.from_wav(wav_file)
    audSeg.export(mp3_file, format="mp3")
    
    #remove mp3 file
    os.remove(wav_file)
    