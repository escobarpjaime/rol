#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

class Mensaje:
    def __init__(self, src, dst, type, data):
        self.src = src
        self.dst = dst
        self.type = type
        self.data = data

    def to_json(self):
        d = {'src': self.src, 'dst': self.dst, 'type': self.type, 'data': self.data}
        j = json.dumps(d)
        return j

class Cliente:
    def __init__(self, websocket):
        self.id = next(num_cliente)
        self.websocket = websocket
        self.mensajes = set()
        self.alias = "Usuario " + str(self.id)
        self.mensajes.add(Mensaje(0,self.id,"wellcome","Eres el cliente " + str(self.id)))

    def setAlias(self, alias):
        self.alias = alias

def get_num_cliente():
    num_cliente = 0
    while True:
        num_cliente += 1
        yield num_cliente

num_cliente = get_num_cliente()

clientes = set()
count = 0

async def add_client(websocket):
    cliente = Cliente(websocket) 
    clientes.add(cliente)
    #await enviar(cliente)
    return cliente

async def rem_client(cliente):
    clientes.remove(cliente)

async def recibir(cliente):
    while True:
        async for mensaje in cliente.websocket:
            m = json.loads(mensaje)
            print("Recibido: " , m)
            if m['type'] == "msg":
                for c in clientes:
                    c.mensajes.add(Mensaje(m['src'], m['dst'], m['type'], "<b>" + str(cliente.alias) + "</b>: " + m['data']))
            elif m['type'] == "alias":
                cliente.alias = m['data']
                #cliente.setAlias(m['data'])
                print("Recibido alias: " , cliente.alias)
        await asyncio.sleep(0.1)

async def gestor_envios(cliente):
    print("gestor_envios")
    ret = 0
    while len(cliente.mensajes) == 0:
       await asyncio.sleep(0.1)
    ret = cliente.mensajes.pop()
    return ret

async def enviar(cliente):
    while True:
        mensaje = await gestor_envios(cliente)
        await cliente.websocket.send(mensaje.to_json())
        await asyncio.sleep(1)

async def ws_main(websocket, path):
    cliente = await add_client(websocket)
    try:
        tarea_recibir = asyncio.ensure_future(recibir(cliente))
        tarea_enviar = asyncio.ensure_future(enviar(cliente))

        #done, pending = await asyncio.wait(
        await asyncio.wait(
            [tarea_recibir, tarea_enviar],
            return_when=asyncio.FIRST_COMPLETED,
        )

        #await asyncio.gather([tarea_recibir, tarea_enviar])

        #for task in pending:
        #    print(task)
        #    task.cancel()
    finally:
        print("REM")
        await rem_client(cliente)

async def main():
    print("hola")
    ws = websockets.serve(ws_main, "localhost", 6789)
    print("hola ws")
    await ws
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
