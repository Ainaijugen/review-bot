import logging
from websocket_server import WebsocketServer


# Called when a client sends a message
def message_received(client, server, message):
    if len(message.split()) != 2:
        return
    request = message.split()[1]
    if message.split()[0][0] == "r":
        # TODO
        answer = ["很棒", "不错", "好美", "开玩笑的", "这只是测试"]
        server.send_message_to_all("magic".join(answer))
    else:
        # TODO
        answer = "0_0"
        server.send_message_to_all(answer)


server = WebsocketServer(34567, host='localhost')
server.set_fn_message_received(message_received)
server.run_forever()
