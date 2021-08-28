#Importamos librerias audio y grabación
import pyaudio
import wave
#Importamos librerias para eliminar o guardar el archivo 
import os
#Importamos librerias Publisher
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Definimos parametros
formato= pyaudio.paInt16
canal=1
cantidad=10000 
velocidad=44100 
duracion= float(input('Indroduce el tiempo de grabacion (segundos): '))
archivo="raw.wav"

#Iniciamos "pyaudio"
audio=pyaudio.PyAudio()
stream=audio.open(format=formato, channels=canal, rate=velocidad, input=True, frames_per_buffer=cantidad)

#Realizamos grabacion
print("Grabando...")
frames=[]
for i in range(0, int(velocidad / cantidad * duracion)): 
    data=stream.read(cantidad)
    frames.append(data)
print("Audio Grabado")

#Detenemos grabacion
stream.stop_stream()
stream.close()
audio.terminate()

# Creamos/Guardamos el archivo de audio  
waveFile = wave.open(archivo,'wb')
waveFile.setnchannels(canal)
waveFile.setsampwidth(audio.get_sample_size(formato))
waveFile.setframerate(velocidad)
waveFile.writeframes(b''.join(frames))
waveFile.close() 

# Guardamos o no el archivo RAW audio  
save_raw_file = input('Desea guardar el audio RAW en el Edge (si/no): ')

if save_raw_file == 'no': 
    print('Audio RAW no guardado')
else:
    print('Audio RAW guardado')

# Llamamos al archivo filtered 
from filtered import filtered_audio
filtered = "filtered.wav"
filtered_audio(archivo, filtered)

# Eliminar archivo RAW audio 
if save_raw_file == 'no': 
    os.remove(archivo)

# Definimos parametros, Publisher
topic = "audio_channel"
host = input('Introduce la dirección IP, de tu dispositivo: ')
port = 1883

f = open(filtered, "rb")
imagestring = f.read()
f.close()
byteArray = bytearray(imagestring)
publish.single(topic, byteArray, hostname=host)

os.remove(filtered)
print('Audio procesado enviado')