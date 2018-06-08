import logging
from websocket_server import WebsocketServer
import JVM.train.test as test
import threading

threadLock = threading.Lock()


# Called when a client sends a message
def message_received(client, server, message):
    if len(message.split()) != 2:
        return
    request = message.split()[1]
    threadLock.acquire()
    if message.split()[0][0] == "r":
        id = int(request.split('_')[0]) * 4 + int(request.split('_')[1])
        answer = test.inference(id, 70)
        server.send_message_to_all("magic".join(answer))
    else:
        # TODO
        answer = "2_3"
        server.send_message_to_all(answer)
    threadLock.release()


server = WebsocketServer(34567, host='localhost')
server.set_fn_message_received(message_received)
server.run_forever()
