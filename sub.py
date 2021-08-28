#Importamos librerias Suscriber
import paho.mqtt.client as mqtt

# Definimos parametros
topic = "audio_channel"
host = "192.168.1.250"
port = 1883

# Creamos conexion
def on_connect(client, userdata, flags, rc):
  client.subscribe(topic)

# Definimos instancia del cliente
client = mqtt.Client()
client.connect(host,port,60)
client.on_connect = on_connect

# Recibe los mensajes y los guarda en el directorio
def on_message(client, userdata, msg):
    f = open("grabacion_recibida.wav", "+wb")
    f.write(msg.payload)
    f.close()
    client.disconnect()
    print("Grabacion recibida y guardada")

client.on_message = on_message
client.loop_forever()