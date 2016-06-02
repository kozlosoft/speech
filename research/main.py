# coding=UTF-8
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import math

import numpy
from setuptools.command.bdist_egg import analyze_egg

rate = 16000

def draw_fft(file_path):
    fs, data = wavfile.read(file_path) # load the data
    a = data.T
    b=[(ele/2**15.) for ele in a] # this is 16-bit track, b is now normalized on [-1,1)
    # # 16000 - значений - звук с сэмплрейт 16000 герц
    # # умножаем аргумент синуса таким образом, чтобы за секунду было 40 полных периодов синуса
    # # это создание ситуации, когда записана секунда звука с частотой 40 герц.
    # # fft дает нам единственное ненулевое значений в индексе 40, равное 8000.
    # # 8000 - это половина сэплрэйта. Половина сэмплрейта - это максимальная похожесть. ЧТО НАМ И ХОТЕЛОСЬ
    # b = [math.sin(x / (rate/ 40. / (math.pi * 2))) for x in range(rate)]

    c = fft(b) # calculate fourier transform (complex numbers list)
    d = len(c) / 2  # you only need half of the fft list (real signal symmetry)
    answer = abs(c[:d])
    # answer = numpy.log(answer)
    # answer = abs(answer)
    return answer

fft_a1 = draw_fft('a.wav')
fft_a2 = draw_fft('a2.wav')
# fft_a1 = draw_fft('aaa_with_empty_before.wav') # SAME FILES - THIS WAS A TRIUMPH. I'M MAKING A NOTE HERE HUGE SUCCESS
# fft_a2 = draw_fft('aaa_without_empty_before.wav')
fft_b1 = draw_fft('aaa_with_empty_before.wav')
# fft_b1 = draw_fft('b.wav')
fft_b2 = draw_fft('b2.wav')

"""
# (len(fft_a1) / float(rate)) - длина файла в секундах
x / (len(fft_a1) / float(rate)) - нормализованные иксы от 0 до 16000
таким образом мы просто сжали график до 0 - 16000
"""
plt.plot([x / (len(fft_a1) / float(rate)) for x in range(1, 1+ len(fft_a1))], fft_a1,'g')
plt.plot([x / (len(fft_a2) / float(rate)) for x in range(1, 1+ len(fft_a2))], fft_a2,'y')
plt.plot([x / (len(fft_b1) / float(rate)) for x in range(1, 1+ len(fft_b1))], fft_b1,'r')
plt.plot([x / (len(fft_b2) / float(rate)) for x in range(1, 1+ len(fft_b2))], fft_b2,'b')
plt.show()
