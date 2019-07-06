import sys
import pyaudio
import wave
import struct
import aubio
import audioop
import math
import numpy as np 
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

#linking together
import KeyChart

FRAME_SIZE = 1024 * 2
FRAMES_PER_FFT = 16 # FFT = Fast Fourier Transform
# FORMAT = pyaudio.paInt16 # Bytes per sample
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100 # Samples per second
CHUNK = 1024 # Number of data samples (Bytes)
RECORD_SECONDS = 5
TOLERANCE = 0.8
# WAVE_OUTPUT = "output.wav"

# I don't really understand FFT 
'''
SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(RATE) / SAMPLES_PER_FFT 
'''

# Open the stream
p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = CHUNK
)


if len(sys.argv) > 1: # If file-name specified on cmdline
    WAVE_OUTPUT_NAME = sys.argv[1] # output file with this name
    outputsink = aubio.sink(WAVE_OUTPUT_NAME, RATE)

# Aubio's Pitch Recognition
fDetection = aubio.pitch("default", 2048, 1024, RATE)
fDetection.set_unit("Hz")
fDetection.set_silence(-40)
fDetection.set_tolerance(TOLERANCE)




print("* RECORDING")

frames = []

NUM_CHUNKS = int((RATE / CHUNK) * RECORD_SECONDS)

'''
# RATE * TIME_RECORDED / CHUNKS = NUM CHUNKS
for i in range(0, NUM_CHUNKS): 
    data = stream.read(CHUNK)
    frames.append(data)
'''

while True:
    try: 
        data = stream.read(CHUNK)
        samples = np.fromstring(data, dtype = aubio.float_type)
        freq = fDetection(samples)[0]
        confidence = fDetection.get_confidence()
        #volume = np.sum(samples**2)/len(samples)
        #f_volume = "{:.6f}".format(volume)
        #rms = audioop.rms(data,1)
        #decibel = 20 * np.log10(rms) #dB = 20 * log10(Amp)
        #print(decibel)
        #uncomment to print original stuff
        #print("{} / {} / {}".format(freq, confidence, f_volume))

        # if note is too low, don't print
        if(freq > 25.0):
           #call KeyChart
           idx = KeyChart.findNote(freq)
           KeyChart.alternate(idx) 

    except KeyboardInterrupt:
        print ("User Ctrl+C. Exiting...")
        break



print("* RECORDING STOPPED")


stream.stop_stream()
stream.close()
p.terminate()

'''
wf = wave.open(WAVE_OUTPUT, 'wb') # writeback
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
'''
'''
data = stream.read(CHUNK)
data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype = 'b') + 127

fig, ax = plt.subplots()
ax.plot(data_int, '-')
plt.show()
'''
