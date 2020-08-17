import asyncio

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

#Данный код создает tcp-соединение для адреса 127.0.0.1:8181 и слушает все входящие запросы.
class ClientServerProtocol(asyncio.Protocol):
    metrics = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        if data.startwith('put'):
            non, name, value, timestamp = data.split()
            if name not in ClientServerProtocol.metrics:
                ClientServerProtocol.metrics[name] = [(timestamp, value)]
            else:
                ClientServerProtocol.metrics[name].append((timestamp, value))
            return 'ok\n\n'
        elif data.startswith('get'):
            _, name = data.split(' ')
            return self.get_metrics(name)
        else:
            return 'error\nwrong command\n\n'

    def get_metrics(self, key):
        resp = 'ok'
        if key == '*':
            for k, v in ClientServerProtocol.metrics.items():
                for metric in v:
                    resp += '\n{key} {value} {timestamp}'.format(key=k, value=metric[1], timestamp=metric[0])
        elif key in ClientServerProtocol.metrics:
            for metric in ClientServerProtocol.metrics[key]:
                resp += '\n{key} {value} {timestamp}'.format(key=key, value=metric[1], timestamp=metric[0])
        resp += '\n\n'
        return resp

if __name__ == '__main__':
    run_server('0.0.0.0', 8888)