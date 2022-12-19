from voice import *

def warp_spectrum(S: np.array, factor: float) -> np.array:
    """Stretch frequency of spectrogram.
    
    Params
    ------
    S: spectrogram
    factor: scaling factor
    """
    #for s in S.T:
        #print((np.arange(0,len(s))/len(s))*factor)
    out_S = np.array([np.interp((np.arange(0, len(s)) / len(s)) * factor,
                               (np.arange(0, len(s)) / len(s)),
                               s)
                      for s in S.T], dtype=complex).T

    return out_S


def shift_freq(x: np.array, alpha: float,
               n_fft=512, hop_length=64) -> np.array:
    """Scale frequency of the data.
    
    Params
    ------
    x: audio data
    alpha: scaling factor
    n_fft: FFT points
    hop_length: jump length 
    
    Returns
    -------
    syn_x: synthesized data
    """
    S1 = librosa.stft(x, n_fft=n_fft, hop_length=hop_length)
    S2 = warp_spectrum(S1, alpha**(1/3)+0.06)
    syn_x = librosa.istft(S2, hop_length=hop_length, win_length=n_fft)

    return syn_x

def frequency_stretching(input_file, alpha):
    data, sr = librosa.load(input_file)
    shifted_data = shift_freq(data, alpha)
    
    sf.write('frequency_stretched_audio.wav', shifted_data, sr)
    