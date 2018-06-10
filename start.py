import logging
from websocket_server import WebsocketServer
import JVM.train.test as test
import threading
import classifier.match as match
import random
import chardet
import urllib.request
import os
import classifier.photo_classify as photo_classify

threadLock = threading.Lock()


# Called when a client sends a message
def message_received(client, server, message):
    message = message.strip()
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
        answer = ""
        if os.path.exists(request):
            answer1 = photo_classify.read_picture(request)
            max_proba = 0
            for x in answer1:
                ans, proba = match.query(x)
                print(ans, "svm: ", proba, "baidu: ", answer1[x])
                if max_proba < proba:
                    max_proba = proba
                    answer = ans
        else:
            answer, _ = match.query(request)
        print(answer)
        if answer[-1] == '5':
            answer = "_".join([answer.split('_')[0], str(random.randint(0, 3))])
        server.send_message_to_all(answer)
    threadLock.release()


server = WebsocketServer(34567, host='localhost')
server.set_fn_message_received(message_received)
server.run_forever()
