# coding=UTF-8
"""
Рисеч.
В этой папке есть несколько звуковых файлов.
Цель - придумать как их отличать.

Я почитал что пишут в интернете, а пишут там про быстрое преобразование фурье, которое позволяет получить коэфиценты
разложения исходной функции( у нас это звуковые волны) на синусоиды, которые в сумме и дадут исходную функцию.

После этого понятнее не стало как нам пригодится fft, поэтому был проведен опыт, чтобы явнее стал физический смысл
fft в контексте звука:
Была сгенерирована секунда звука на частоте 40 герц с сэмплрэйтом 16000.
Это означает что имеется массив из 16000 значений звуковой функции, где в значениях синус, который делал
40 полных периодов. Иными словами - 40 горбов в положительной части графика на участке 0 - 16000.
Этот массив был отправлен в fft, и fft вернул массив из 16000 результатов. Все они были 0, кроме индекса
40. В индексе 40 было значение 8000.
После этого fft было скормлено 2 секунды такого звука, и ответ был мощностью 32000 с 8000 в индексе 80. Если
отобразить 32000 значений на ось икс [0; 16000] мы получим такой же реультат, как и в первом прогоне на секунде.
Отсюда был сделан вывод, что fft в индексе i скажет нам какой частоты звук был в исходном массиве(т.е. i = частота в
герцах), а близость к половине сэмплрейта у fft[i] - похожесть исходной частоты на частоту i.

Решение - чтобы достичь цели я предлагаю отличать буквы по их спектру частот.

Описание файлов:
* a.wav -  произнесенная буква а
* a2.wav - другая запись буквы а
* b.wav - произнесенная буква б
* b2.wav - другая запись буквы б

"""
import matplotlib.pyplot as plt
import numpy
from scipy import interpolate
from scipy.fftpack import fft
from scipy.io import wavfile  # get the api


def generate_spectrum(file_path):
    rate, data = wavfile.read(file_path)  # считываем wav 16 бит 16000Hz mono
    samples = data.T
    # насколько я понял у всех принято делать нормализацию входных данных, и я тоже решил сделать
    normalized_samples = [(sample / 2 ** 15.) for sample in
                          samples]  # нормализация на [-1,1]; 2**15 т.к. знаковые 16 бит
    transformed_samples = fft(normalized_samples)  # быстрое преобразование фурье
    # оставляем половину значений т.к. результат симметричен, относительно середины массива
    transformed_samples = transformed_samples[:len(transformed_samples) / 2]
    # берем по модулю т.к. не бывает отрицательного кол-ва периодов
    transformed_samples = abs(transformed_samples)

    # сожмем получившийся график по иксу, чтобы он влезал в частоту
    x_values = [x / (len(transformed_samples) / float(rate)) for x in range(len(transformed_samples))]
    # интерполируем график на целочисленную шкалу иксов - таким образом она приобретет семантику частоты,
    # а значения трансф. сэмплов станут степенью похожести на эту частоту, где максимальная похожесть выражена как
    # rate (максимальная частота в wav-файле)
    interpolator = interpolate.interp1d(x_values, transformed_samples)
    frequency = numpy.arange(1, int(max(x_values)), 1)  # int(max(x_values)) примерно равно rate.
    # и не равно rate оно здесь т.к. мы не можем интерполировать функцию вне изначального диапазона иксов
    spectrum = interpolator(frequency)

    return spectrum


def print_a1_vs_other_errors(spectrum_a1, spectrum_a2, spectrum_b1, spectrum_b2):
    # посчитаем накопленную ошибку между буквами
    # сравним первый сэмпл а со вторым а, и двумя б - на всех частотах
    overall_error_a1_a2 = 0
    overall_error_a1_b1 = 0
    overall_error_a1_b2 = 0
    for i in range(min(len(spectrum_a1), len(spectrum_a2), len(spectrum_b1), len(spectrum_b2))):
        overall_error_a1_a2 += abs(spectrum_a1[i] - spectrum_a2[i])
        overall_error_a1_b1 += abs(spectrum_a1[i] - spectrum_b1[i])
        overall_error_a1_b2 += abs(spectrum_a1[i] - spectrum_b2[i])
    overall_error_list = (overall_error_a1_a2, overall_error_a1_b1, overall_error_a1_b2)
    if overall_error_a1_a2 is min(overall_error_list):
        print "overall error shows that a1 more like a2 than b\'s"
        print "\terrors a1 vs a2, b1, b2: " + str(overall_error_list)
        print ""

    # сравним а, но только на голосовом диапазоне
    human_voice_frequency_range = range(300, 3400)
    human_voice_error_a1_a2 = 0
    human_voice_error_a1_b1 = 0
    human_voice_error_a1_b2 = 0
    for i in human_voice_frequency_range:
        human_voice_error_a1_a2 += abs(spectrum_a1[i] - spectrum_a2[i])
        human_voice_error_a1_b1 += abs(spectrum_a1[i] - spectrum_b1[i])
        human_voice_error_a1_b2 += abs(spectrum_a1[i] - spectrum_b2[i])
    human_voice_error_list = (human_voice_error_a1_a2, human_voice_error_a1_b1, human_voice_error_a1_b2)
    if human_voice_error_a1_a2 is min(human_voice_error_list):
        print "human voice frequency range error shows that a1 more like a2 than b\'s"
        print "\terrors a1 vs a2, b1, b2: " + str(human_voice_error_list)


spectrum_a1 = generate_spectrum('a.wav')
spectrum_a2 = generate_spectrum('a2.wav')
spectrum_b1 = generate_spectrum('b.wav')
spectrum_b2 = generate_spectrum('b2.wav')

print_a1_vs_other_errors(spectrum_a1, spectrum_a2, spectrum_b1, spectrum_b2)

plt.plot(spectrum_a1, 'g')
plt.plot(spectrum_a2, 'y')
plt.plot(spectrum_b1, 'r')
plt.plot(spectrum_b2, 'b')
plt.show()
