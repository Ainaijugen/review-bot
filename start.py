import logging
from websocket_server import WebsocketServer
import JVM.train.test as test
import threading
import classifier.match as match
import random
import chardet
import urllib.request

threadLock = threading.Lock()


# Called when a client sends a message
def message_received(client, server, message):
    if len(message.split()) != 2:
        request = "".join(message.split()[1:])
    else:
        request = message.split()[1]
    threadLock.acquire()
    request = urllib.request.unquote(request)
    print(request)
    # result = chardet.detect(request)
    # print(result)
    if message.split()[0][0] == "r":
        id = int(request.split('_')[0]) * 4 + int(request.split('_')[1])
        answer = test.inference(id, 70)
        server.send_message_to_all("magic".join(answer))
    else:
        answer = match.query(request)
        print(answer)
        if answer[-1] == 'x':
            answer = "_".join([answer.split('_')[0], str(random.randint(0, 3))])
        server.send_message_to_all(answer)
    threadLock.release()


server = WebsocketServer(34567, host='localhost')
server.set_fn_message_received(message_received)
server.run_forever()
