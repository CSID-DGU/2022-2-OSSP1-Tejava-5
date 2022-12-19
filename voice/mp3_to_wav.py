from pydub import AudioSegment
import os

def mp3_to_wav(extracted_mp3):
    #files
    mp3_file = extracted_mp3
    wav_file = "extracted_wav_audio.wav"
    
    #convert mp3 file to wav file
    audSeg = AudioSegment.from_mp3(mp3_file)
    audSeg.export(wav_file, format="wav")
    
    #remove mp3 file
    os.remove(mp3_file)
    