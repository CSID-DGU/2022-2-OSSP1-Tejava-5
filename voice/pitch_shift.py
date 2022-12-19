from voice import *

def butter_lowpass(cutoff: float, fs: int, order: int=3) -> tuple:
    """Find lowpass filter coefficients.
    
    Params
    ------
    cutoff: cutoff frequency in Hz
    fs: sampling frequency in Hz
    order: filter coefficient size
    
    Returns
    -------
    (b, a): numerator and denominator polynomials of the IIR filter.
    
    """
    b, a = signal.butter(order, cutoff, btype='low', fs=fs, analog=False)
    
    return (b, a)


def butter_lowpass_filter(data: np.array, cutoff: float, fs: int, order: int=3) -> np.array:
    """Apply lowpass filter to audio data to remove aliasing effect. Used for preprocessing step.
    
    Params
    ------
    data: audio data of 0.5 second length
    cutoff: cutoff frequency in Hz
    fs: sampling frequency in Hz
    order: filter coefficient size
    
    Returns
    -------
    y: lowpass filtered audio data
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    
    return y


def frameize(x: np.array, N: int, H_a: int, hfilt: np.array) -> list:
    """Truncate audio sample into frames.
    
    Params
    ------
    x: audio array
    N: segment size
    H_a: analysis hop size
    hfilt: windowing filter
    
    Returns
    -------
    frames: segments of audio sample
    """
    frames = []
    idx = 0 
    
    while True:
        try: frames += [hfilt*x[H_a*idx:H_a*idx+N]]
        except: break   
        idx += 1
    
    return frames


def find_hfilt_norm(hfilt: np.array, H_s: int, delta: int=0) -> np.array:
    """Compute normalization filter array for windowing effect.
    
    Params
    ------
    hfilt: filter window used for our purpose
    H_s: synthesis hop size
    delta: small shift for synchronization
    
    Returns
    -------
    hf_norm: normalization filter array 
    """
    hf_norm = copy(hfilt)
    N = len(hfilt)
    
    if (H_s+delta) < N and (H_s+delta) >= 0:
        # add right superposed
        hf_norm[(H_s+delta):] += hfilt[:N-(H_s+delta)]
        # add left superposed
        hf_norm[:N-(H_s+delta)] += hfilt[(H_s+delta):]
        
    return hf_norm

    
def scale_time(x: np.array, N: int, H_a: int,
                 hfilt: np.array, alpha: float) -> np.array:
    """Scale time of audio sample by given ratio.
    
    Params
    ------
    x: audio data
    N: segment size
    H_a: analysis hop size
    hfilt: windowing filter
    alpha: time-scaling factor
    
    Returns
    -------
    out_x: time-scaled data 
    """
    # put into frames
    frames = frameize(x, N, H_a, hfilt)
    
    
    H_s = int(np.round(H_a*alpha))
    out_x = np.zeros(len(frames)*H_s+N)

    # time-scaling
    for i, frame in enumerate(frames):
        hfilt_norm = find_hfilt_norm(hfilt, H_s)    
        out_x[i*H_s:i*H_s+N] += frame/hfilt_norm

    return out_x

def synthesize_pitch(x: np.array, sr: int, N: int, H_a: int,
                      hfilt: np.array, alpha: float) -> np.array:
    """Synthesize sound sample into new one with different pitch using PSOLA algorithm.
    
    Params
    ------
    x: audio data
    sr: sampling rate
    N: segment size
    H_a: analysis hop size
    hfilt: windowing filter
    alpha: pitch factor
    
    Returns
    -------
    syn_x: synthesized data
    """
    syn_x = scale_time(x, N, H_a, hfilt, alpha)
    
    # apply anti-aliasing
    if alpha >= 1: syn_x = butter_lowpass_filter(syn_x, sr/2*(1/alpha)*0.6, fs=sr, order=3)

    # resampling
    syn_x = samplerate.resample(syn_x, 1/alpha, 'sinc_best')
    syn_x = syn_x/np.max(abs(syn_x))
        
    return syn_x

def pitch_shift(input_file, alpha):
    data, sr = librosa.load(input_file)

    # make segments of 0.05-seconds (2205)
    N = 1024 # segment size for sampling rate 44100 Hz
    H_a = int(N*0.6) # analysis hop size between 0.5 ~ 1
    hfilt = np.hanning(N) # filter type

    shifted_data = synthesize_pitch(data, sr, N, H_a, hfilt, alpha)
    sf.write('pitch_shifted_audio.wav', shifted_data, sr)
    
    os.remove(input_file)