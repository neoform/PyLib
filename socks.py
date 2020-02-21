from __future__ import annotations
import socket
import socketserver
import threading


ServerAddress = ("127.0.0.1", 6060)


class MyTCPClientHandler(socketserver.StreamRequestHandler):

    def handle(self):
        thread_name = threading.current_thread().name
        msg         = self.rfile.readline().strip()
        print(f"{thread_name} - {self.client_address[0]}: {msg}")


class MyServer:

    def __init__(self):
        socketserver.ThreadingTCPServer.request_queue_size = socket.SOMAXCONN
        socketserver.ThreadingTCPServer.allow_reuse_address = True

        self._server        = socketserver.ThreadingTCPServer(ServerAddress, MyTCPClientHandler)
        self._server_thread = threading.Thread(target=self._serve)

    def __del__(self):
        if self._server_thread.isAlive():
            self._server_thread.join(timeout=10)

    def _serve(self):
        try:
            self._server.serve_forever()
        except Exception as e:
            print(e)

    def start(self):
        if not self._server_thread.isAlive():
            print("Starting server")
            self._server_thread.start()

    def stop(self):
        print("Stopping server")
        self._server.shutdown()


server = MyServer()
server.start()

input("Enter please")

server.stop()