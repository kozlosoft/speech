# speech
Распознователь речи, сделанный за несколько вечеров.
Решение использует спектр, полученный быстрым преобразованием Фурье. 

## Постановка задачи
Я на микрофоне ноутбука, в относительно тихой комнате записываю
произношение букв алфавита. Нужно сделать приложение, которое позволит
для еще раз записанных мною букв в тех же условиях определить - что 
за буква алфавита была мною произнесена. 

Входные данные: wav signed 16 PCM mono

## Содержимое проекта
Два исполняемых файла:

* ./research/main.py - описание творческой части решения задачи.
Там масса комментариев на русском языке. 
Там получена экспортируемая функция генерации частотного спектра, и 
выводятся графики спектров рисеч образцов звука:
![Research](./data/images/research.png)


* main.py - скрипт решающий описанную задачу. 
Сдержанные комментарии на английском языке. 
Производится чтение эталонов, затем входных файлов звука - 
файлы сравниваются по частотным спектрам и выводится решение - 
какая все таки буква произнесена в файле. 
К слову, я честный, поэтому скрывать тот факт что 
вместо "д" распозналась "и" не стал. Тем более что оставшиеся три
буквы распознались правильно =)
![Main](./data/images/main_algo.png)

## Requirements

* Python 3.4
* matplotlib
* numpy
* scipy

run:

* python ./main.py
* cd ./research/ && python main.py

### windows
Download and install python 3.4.* (add it to path during installation)

Download numpy_mkl from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
for example: numpy-1.11.0+mkl-cp34-cp34m-win_amd64.whl

Download *whl for your platform from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
for example: scipy-0.17.1-cp34-cp34m-win_amd64.whl

run command prompt as administrator:

* pip install --upgrade pip
* python -m pip install matplotlib
* pip install "numpy-1.11.0+mkl-cp34-cp34m-win_amd64.whl"
* pip install scipy-0.17.1-cp34-cp34m-win_amd64.whl

### ubuntu
sudo apt-get install python3.4 python3-matplotlib python3-scipy
