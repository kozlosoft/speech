import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api

def draw_fft(file_path):
    fs, data = wavfile.read(file_path) # load the data
    a = data.T
    b=[(ele/2**16.) for ele in a] # this is 16-bit track, b is now normalized on [-1,1)
    c = fft(b) # calculate fourier transform (complex numbers list)
    d = len(c) / 2  # you only need half of the fft list (real signal symmetry)
    return abs(c[:(d-1)])

fft_a1 = draw_fft('a.wav')
fft_a2 = draw_fft('a2.wav')
fft_b1 = draw_fft('b.wav')
fft_b2 = draw_fft('b2.wav')

print max(fft_a1)
print min(fft_a1)

diff_between_a = 0
diff_between_b = 0
diff_between_a1_b1 = 0
diff_between_a2_b2 = 0
for i in range(1000):
    diff_between_a += abs(fft_a1[i] - fft_a2[i])
    diff_between_b += abs(fft_b1[i] - fft_b2[i])
    diff_between_a1_b1 += abs(fft_a1[i] - fft_b1[i])
    diff_between_a2_b2 += abs(fft_a2[i] - fft_b2[i])

print("diff_between_a " + str(diff_between_a))
print("diff_between_b " + str(diff_between_b))
print("diff_between_a1_b1 " + str(diff_between_a1_b1))
print("diff_between_a2_b2 " + str(diff_between_a2_b2))

plt.plot(fft_a1,'g')
plt.plot(fft_a2,'y')
plt.plot(fft_b1,'r')
plt.plot(fft_b2,'b')
plt.show()
