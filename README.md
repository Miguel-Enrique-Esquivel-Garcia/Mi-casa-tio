# 🏠 Mi-casa-tio — Sistema Domótico Integral con ESP32 y MicroPython

Este documento describe en detalle el funcionamiento, propósito, arquitectura y proceso de instalación del sistema domótico Mi-casa-tio, un proyecto desarrollado con un ESP32, programado completamente en MicroPython y diseñado para ofrecer un ejemplo funcional y extendido de cómo implementar automatización básica en un entorno doméstico utilizando sensores, actuadores y comunicación basada en MQTT.

El objetivo de este proyecto es proporcionar un modelo educativo, práctico y realista de un sistema domótico, integrando tecnologías de red, lectura de sensores ambientales, activación automática de actuadores y control remoto mediante protocolos IoT modernos.

# 🔧 1. Introducción General al Proyecto
El proyecto Mi-casa-tio representa un sistema domótico completo donde un solo ESP32 opera como unidad central encargada de:

-Recibir órdenes remotas por MQTT.
-Monitorear continuamente varios sensores ambientales.
-Activar actuadores en tiempo real dependiendo de las condiciones detectadas.
-Mantener comunicación estable mediante WiFi.
-Responder ante eventos críticos como gas, lluvia o temperatura elevada.

Este sistema puede ser replicado, ampliado y modificado para clases, prácticas, proyectos académicos o implementaciones experimentales de IoT.

# 🧰 2. Requisitos del Hardware
Requisitos del Hardware

-ESP32 (cualquier modelo con ADC y WiFi)
-Sensor MQ-2
-Sensor de lluvia (digital)
-Sensor DHT11
-Servo SG90 o similar
-Relevador de 5V
-Buzzer activo
-Ventilador de 2" 
-Fuente de alimentación estable
-Cables jumpers y protoboard


# ⚙️ 3. Funcionalidades del Sistema
A continuación se describen de manera profunda las funciones que implementa el archivo main.py.
# 🔥 3.1 Detección de Gas (MQ-2)
El sensor MQ-2, conectado al GPIO 36 mediante ADC, monitorea permanentemente el nivel de concentración de gases inflamables o humo. Su lectura se usa para activar mecanismos de seguridad:

Si la lectura supera el umbral establecido (550 en este caso), el sistema ejecuta:
-Activación del buzzer para emitir una alerta sonora inmediata.
-Encendido del relevador, que puede accionar un ventilador o extractor para expulsar aire contaminado o reducir riesgos.

-Si el nivel baja y la temperatura está en condiciones normales, el relevador se apaga automáticamente.

Esta función constituye un pilar esencial de la seguridad doméstica automatizada.

# 🌧 3.2 Sensor de Lluvia + Control de Ventana con Servo
El sensor de lluvia conectado al GPIO 3 opera como entrada digital. El sistema utiliza su lectura para mover un servomotor en GPIO 13 capaz de abrir o cerrar una ventana automática:

Cuando se detecta lluvia:
El sistema asume condiciones ambientales externas adversas y procede a cerrar la ventana moviendo el servo al ángulo de cierre.

Cuando no hay lluvia:
El servo regresa la ventana a su posición abierta, permitiendo flujo de aire.

Este componente introduce automatización física visible y configurable dentro del proyecto.

# 🌡 3.3 Sensor DHT11 (Temperatura y Humedad)
El sensor DHT11, conectado al GPIO 14, proporciona datos ambientales esenciales utilizados para activar ventilación automática:

-Si la temperatura es mayor o igual a 30°C, el ESP32 activa el relevador, encendiendo el ventilador o extractor.
-Si la temperatura desciende, el sistema apaga el relevador, siempre y cuando no haya presencia de gas medida por el MQ-2.

Esto genera un sistema inteligente que analiza simultáneamente múltiples condiciones para actuar.

# 💡 3.4 Control de LED mediante MQTT
El sistema se conecta al broker MQTT especificado y se suscribe al tópico:

casa/sala/led

El LED en el GPIO 21 se conecta al relevador y responde a mensajes:
-ON → Enciende el LED
-OFF → Apaga el LED

Esto permite que cualquier aplicación que publique mensajes en el tópico controle el dispositivo de manera remota.

# 🔊 3.5 Buzzer y Relevador
Ambos componentes están ligados a eventos críticos:
Buzzer (GPIO 15):
Actúa como alerta sonora del sistema ante condiciones de gas.
Se activa cuando:
-Hay gas

Relevador (GPIO 5):
Puede controlar un ventilador, extractor o dispositivo de 120/220 V.
Se activa cuando:
-La temperatura supera el límite

Este diseño permite que el sistema reaccione por múltiples causas posibles.

# 📡 4. Comunicación y Conectividad
# 📶 4.1 Conexión WiFi
El ESP32 conecta automáticamente a la red configurada mediante las constantes:

WIFI_SSID
WIFI_PASSWORD


Si falla la conexión, el sistema reintenta por un tiempo definido.
En caso de no lograrlo, lanza un error que reinicia el microcontrolador.

# 📡 4.2 Comunicación mediante MQTT
El sistema se conecta al broker definido en MQTT_BROKER.

Utiliza el puerto estándar 1883.

Se suscribe al tópico para control de LED.

Revisa mensajes continuamente con check_msg().

MQTT es el corazón del control remoto del proyecto.

# 🧩 5. Detalles del Funcionamiento Interno
El programa entra en un ciclo infinito donde:

-Revisa mensajes MQTT.
-Lee valor de gas.
-Activa actuadores según resultados.
-Revisa lluvia y ajusta servo.
-Mide temperatura y humedad.
-Enciende/apaga relevador según lógica de seguridad.
-Muestra en consola todos los valores leídos.
-Repite todo cada segundo.

Este comportamiento crea un sistema reactivo, autónomo y confiable.

# 📁 6. Instalación y Carga del Código
Aunque MicroPython no usa requirements del mismo modo que un entorno normal, también se incluyen instrucciones para manipulación desde PC.

# 📌 6.1 Instalación de Herramientas en PC
pip install esptool adafruit-ampy

# 📌 6.2 Listar librerías instaladas
pip list

# 📌 6.3 Exportar requirements.txt
pip freeze > requirements.txt

# 📌 6.4 Instalar dependencias del archivo
pip install -r requirements.txt

# 📌 6.5 Subir código al ESP32
ampy --port COM6 put main.py

# 📌 6.6 Borrar memoria del ESP32 (opcional)
esptool --port COM6 erase-flash

# ▶️ 7. Ejecución del Sistema
Una vez cargado el archivo main.py, el ESP32:

-Se reinicia.
-Conecta a la red WiFi.
-Conecta al broker MQTT.
-Inicializa sensores y actuadores.
-Muestra estado inicial.
-Comienza el ciclo de monitoreo.
-La salida de consola reporta:
-Nivel de gas
-Estado de lluvia
-Movimiento del servo
-Temperatura
-Humedad
-Activación del relé
-Mensajes MQTT

# 📄 8. Licencia
Este proyecto es de uso educativo y se distribuye bajo la licencia MIT.

# 🙌 9. Agradecimientos
Se les agradece a todas las personas que hicieron posible este proyecto:

Mi equipo
Mi mamá
Doctor Bortoni
Mike
El cuyo de Mike
El de los enamorados
La mamá de Ana por no corrernos
El hermano de Ana alias "Jajantahxd8751"
Al gato flaco que nos encontramos en la calle
A los poliperros 
A Santillana 
A los Indios por crear tutoriales 
Al Pirata de Culiacán por inspirarme 
A Shrek
Al comedor Nancy por alimentarnos en nuestros peores momentos
A Maluma 
A Chikis por las good vibes 
A Noe
A los Tigres del norte 
A los corridos
Al café por mantenerme despierto 2 días seguidos 

Y especialmente al profesor Charly Mercury, por su apoyo, explicación, motivación y por impulsar el desarrollo del proyecto
además de responder fuera de horario laboral. Lo amamos grr