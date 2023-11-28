import socket


central_agent_ip = "127.0.0.1"
central_agent_port = 5005


cell_ip = "127.0.0.1"
cell_port = 5006

# Kreiranje  TCP socketa za centralnog agenta
central_agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Povezivanje socketa sa IP i portom centralnog agenta
central_agent_socket.bind((central_agent_ip, central_agent_port))

# Slušanje za nadolazeću konekciju
central_agent_socket.listen(5)

while True:
    # Prihvatanje konekcije sa ćelijom
    cell_socket, addr = central_agent_socket.accept()
    print("Cell connected from IP:", addr[0],"and Port:", addr[1])

    # Primanje podataka od ćelije
    data = cell_socket.recv(1024).decode()
    print("Received message from cell:", data)

    # Slanje odgovora ćeliji
    response = "ACK"
    cell_socket.send(response.encode())
    print("Sent response to cell:", response)
    cell_socket.close()



#UDP PRORTOKOL

import socket

central_agent_ip = "127.0.0.1"
central_agent_port = 5005

# Cell IP and Port
cell_ip = "127.0.0.1"
cell_port = 5006

# Kreiranje UDP socketa za centralnog agenta
central_agent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Povezivanje socketa sa IP i portom centralnog agenta
central_agent_socket.bind((central_agent_ip, central_agent_port))

# Kreiranje UDP socketa za ćeliju
cell_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Primanje podataka od ćelije
    data, addr = central_agent_socket.recvfrom(1024)
    print("Received message from cell:", data)

    # Slanje odgovora ćeliji
    response = "ACK"
    cell_socket.sendto(response.encode(), (cell_ip, cell_port))
    print("Sent response to cell:", response)




#PUBLISH - SUBSCRIBE

import paho.mqtt.client as mqtt

# Kreiranje klijenta za komunikaciju
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)

# Pretplata na temu
client.subscribe('cell/update')

def on_message(client, userdata, msg):
    
    update = json.loads(msg.payload)
    dc = update['dc']
    
    print("Received update: dc = {}".format(dc))

# Callback funkcija
client.on_message = on_message

# Petlja za primanje poruka
client.loop_start()

#MESSAGE QUEUE METODA

import pika

# AMQP parametri za konekicju
amqp_url = "amqp://guest:guest@localhost:5672"

# Konekcija sa  message queue
connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
channel = connection.channel()

# Deklaracija
queue_name = "central_agent"
channel.queue_declare(queue=queue_name)


def callback(ch, method, properties, body):
    print("Received message from cell:", body.decode())
    # Slanje odgovora ćelijama
    response = "ACK"
    channel.basic_publish(exchange='',
                      routing_key=properties.reply_to,
                      body=response)


channel.basic_consume(queue=queue_name,
                      auto_ack=True,
                      on_message_callback=callback)
print("Central Agent is waiting for messages...")
channel.start_consuming()

#RPC METODA SA ASPEKTA CENTRALNOG AGENTA

from xmlrpc.server import SimpleXMLRPCServer

# IP adresa i port centralnog agenta
central_agent_ip = "127.0.0.1"
central_agent_port = 5005

# Kreiranje XML-RPC servera
server = SimpleXMLRPCServer((central_agent_ip, central_agent_port), allow_none=True)

# Definisanje funkcije koju ćelije mogu zvati 
def receive_data_from_cell(data):
    print("Received message from cell:", data)
    return "ACK"

# Registracija funkcije sa servereom
server.register_function(receive_data_from_cell, 'receive_data_from_cell')

# Pokretanje servera
print("Central Agent is waiting for connections...")
server.serve_forever()


#RPC METODA SA ASPEKTA ĆELIJE

import xmlrpc.client


central_agent_ip = "127.0.0.1"
central_agent_port = 5005

# Konekcija sa serverom
with xmlrpc.client.ServerProxy("http://{}:{}/".format(central_agent_ip,central_agent_port)) as proxy:
    # Slanje podataka centralnom agentu
    response = proxy.receive_data_from_cell("Hello, Central Agent!")
    print("Sent message to central agent and received response:", response)
