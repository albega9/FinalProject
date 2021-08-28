#Importamos librerias para calcula la convolucion
import numpy as np 
#Importamos librerias tratar el archivo .wav
import wave 
#Importamos librerias para realizar funciones matemáticas
import math
#Importamos librerias para declaración de la función with
import contextlib

cutOffFrequency = float(input('Indroduce la frecuencia de corte para realizar el filtrado paso bajo(): '))

#calcula la convolucion
def running_mean(x, windowSize):
  cumsum = np.cumsum(np.insert(x, 0, 0)) 
  return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize


def filtered_audio(fname, outname):
    # Descompone los parametros necesarios del archivo wav
    with contextlib.closing(wave.open(fname,'rb')) as spf:
        sampleRate = spf.getframerate()
        ampWidth = spf.getsampwidth()
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()
        
        # Extraer audio Raw. desde archivo WAV multicanal
        signal = spf.readframes(nFrames*nChannels)
        spf.close()

        # Obtenemos los canales
        if ampWidth == 1:
            dtype = np.uint8
        elif ampWidth == 2:
            dtype = np.int16 
        else:
            raise ValueError("Only supports 8 and 16 bit audio formats.")

        channels = np.fromstring(signal, dtype=dtype)
        channels.shape = (nFrames, nChannels)
        channels = channels.T

        # Realizamos el filtro paso bajo y aumentamos la señal
        print('Audio filtrado')
        aum = float(input('Indroduce la amplitud con la que se aumentara la señal procesada (): '))
        freqRatio = (cutOffFrequency/sampleRate)
        N = int(math.sqrt(0.196196 + freqRatio**aum)/freqRatio)

        # Usar media móvil (solo en el primer canal)
        filtered = running_mean(channels[0], N).astype(channels.dtype)

        wav_file = wave.open(outname, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()