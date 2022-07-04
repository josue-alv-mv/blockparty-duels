import socket
import threading


class Network:
    def __init__(self, is_host):
        self.is_host = is_host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 28024
        self.encoding = 'utf-8'
        self.buf_size = 16384
        self.content_splitter = '|'
        self.message_splitter = '\n'
        self.recvd_messages = ReceivedMessages()
        self.active = False

    # def get(self):
    #     # data can be lost if the recv_thread saves a message after this function copies data ? ...
    #     data = self.recvd_messages.copy()
    #     self.recvd_messages.clear()
    #     return data

    def get(self):
        # messages are removed from the queue as they're called by the "for" loop
        return self.recvd_messages

    def send(self, tag, message):
        if self.active:
            full_message = self.content_splitter.join([tag, message]) + self.message_splitter
            encoded_message = full_message.encode(self.encoding)
            
            if self.is_host:
                try:
                    self.client.send(encoded_message)

                except Exception as e:
                    print(e)
                    self.close()

            else:
                try:
                    self.socket.send(encoded_message)

                except Exception as e:
                    print(e)
                    self.close()

    def receive(self):
        while True:
            if self.is_host:
                try:
                    recvd = self.client.recv(self.buf_size).decode(self.encoding)

                except Exception as e:
                    print(e)
                    self.close()
                    break

            else:
                try:
                    recvd = self.socket.recv(self.buf_size).decode(self.encoding)

                except Exception as e:
                    print(e)
                    self.close()
                    break

            # log messages ...
            if recvd.endswith(self.message_splitter):
                print(f'Received: <{recvd[:-1]}>')
            else:
                print(f'Broken message: <{recvd}>')

            while recvd.count(self.message_splitter) > 0:
                tag, text = recvd[:recvd.index(self.message_splitter)].split(self.content_splitter)
                recvd = recvd[recvd.index(self.message_splitter) + 1:]
                self.recvd_messages.append(Message(tag,text))

    def close(self):
        self.socket.close()
        if self.is_host and self.active:
            self.client.close()

        self.active = False


class Client(Network):
    def __init__(self):
        super().__init__(is_host=False)

    def connect(self, address):
        try:
            self.socket.connect((address, self.port))
            self.recv_thread = threading.Thread(target=self.receive, daemon=True)
            self.recv_thread.start()
            self.active = True
            return True

        except Exception as e:
            print("Connection error:", e)
            return False


class Server(Network):
    def __init__(self):
        super().__init__(is_host=True)

    def listen(self):
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen()
        self.accept_thread = threading.Thread(target=self.accept_conn, daemon=True)
        self.accept_thread.start()

    def accept_conn(self):
        while True:
            try:
                client, adress = self.socket.accept()
            except:
                print("Stopping accept_conn thread due to an exception (probably a socket close)")
                break

            print('Connection from:', adress)

            if self.active:
                print("Connection refused! Only 1 client is allowed!")

            else:
                self.client = client
                self.recv_thread = threading.Thread(target=self.receive, daemon=True)
                self.recv_thread.start()
                self.active = True


class ReceivedMessages:
    def __init__(self):
        self.list = []

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.list) == 0:
            raise StopIteration

        message = self.list[0]
        self.list.pop(0)
        return message

    def append(self, message):
        self.list.append(message)


class Message:
    def __init__ (self, tag, text):
        self.tag = tag
        self.text = text