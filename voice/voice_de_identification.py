from mp3_to_wav import mp3_to_wav
from pitch_shift import pitch_shift
from frequency_stretching import frequency_stretching
from db_normalize import db_normalize
from wav_to_mp3 import wav_to_mp3

def voice_de_identification(extracted_audio, alpha):
    mp3_to_wav(extracted_audio) # change extracted mp3 file to wav
    
    pitch_shift("extracted_wav_audio.wav", alpha) # shifting pitch 
    frequency_stretching("pitch_shifted_audio.wav", alpha) # frequency stretching
    
    # db normalize between pitch shifted audio and frequency stretched audio
    db_normalize("pitch_shifted_audio.wav", "frequency_stretched_audio.wav")
    
    wav_to_mp3("normalized_audio.wav") # change normalized wav file to mp3
    
    
# output: de_identified_audio.mp3
