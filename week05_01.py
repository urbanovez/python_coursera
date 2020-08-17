import socket
import time


class ClientError(Exception):
    pass

class Client():
    def __init__(self, ip, host, timeout = None):
        self.ip = ip
        self.host = int(host)
        self.timeout = int(timeout)


    def send(self, ctr):
        sock = socket.create_connection((self.ip, self.host), self.timeout)
        sock.sendall(ctr.encode("utf8"))
        buf = sock.recv(1024)
        sock.close()
        return buf.decode('utf-8')


    def get(self, key):
        resp = self.send('get ' + key + '\n')
        if resp[0:3] != 'ok\n':
            raise ClientError(resp)
        ret = dict()
        lines = resp.split('\n')
        for l in lines[1:-2]:
            metric = l.split(' ')
            res_key = metric[0]
            res_val = float(metric[1])
            res_ts = int(metric[2])
            if not res_key in ret:
                ret[res_key] = list()
            ret[res_key].append((res_ts, res_val))
            ret[res_key].sort(key=lambda tup: tup[0])

        return ret
        

    def put(self, key, value, timestamp = int(time.time())):
        resp = self.send('put ' + key + ' ' + str(value) + ' ' + str(timestamp) + '\n')
        if resp[0:3] != 'ok\n':
            raise ClientError(resp)


