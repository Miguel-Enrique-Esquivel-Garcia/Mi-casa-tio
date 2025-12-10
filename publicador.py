import paho.mqtt.client as mqtt
import mycallbacks

client = mqtt.Client(
    client_id="charly_compu",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_message = mycallbacks.on_message

broker = '10.70.87.205'
myport = 1883
client.connect(broker, port=myport, keepalive=60)

mytopic = 'casa/sala/led'

# Si quieres recibir también mensajes:
# client.subscribe(mytopic)
# client.loop_start()

while True:
    cmd = input("Escribe ON, OFF o EXIT: ").strip().upper()

    if cmd == "EXIT":
        print("Saliendo.")
        break

    if cmd not in ["ON", "OFF"]:
        print("Comando inválido. Usa ON, OFF o EXIT.")
        continue

    result = client.publish(mytopic, cmd)
    if result.rc == 0:
        print(f"Mensaje '{cmd}' enviado.")
    else:
        print("Error enviando mensaje.")