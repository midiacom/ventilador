import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código de resultado {rc}")
    client.subscribe("topic/test")

def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
