import pyaudio
import wave
import struct
import aubio
import numpy as np 
import matplotlib.pyplot as plt

FRAME_SIZE = 1024 * 2
FRAMES_PER_FFT = 16 # FFT = Fast Fourier Transform
# FORMAT = pyaudio.paInt16 # Bytes per sample
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100 # Samples per second
CHUNK = 1024 # Number of data samples (Bytes)
RECORD_SECONDS = 5
WAVE_OUTPUT = "output.wav"

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

# Aubio's Pitch Recognition
pDetection = aubio.pitch("default", 2048, 2048//2, RATE)
pDetection.set_unit("Hz")
pDetection.set_silence(-40)



print("* recording")

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
        pitch = pDetection(samples)[0]
        volume = np.sum(samples**2)/len(samples)
        volume = "{:.6f}".format(volume)

        print(pitch)
        print(volume)

        # Recording
        frames.append(data)
    except KeyboardInterrupt:
        print ("User Ctrl+C. Exiting...")
        break



print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT, 'wb') # writeback
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

'''
data = stream.read(CHUNK)
data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype = 'b') + 127

fig, ax = plt.subplots()
ax.plot(data_int, '-')
plt.show()
'''