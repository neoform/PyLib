import socket
import threading


def spam():
    for i in range(100):
        # Create a socket instance
        with socket.socket() as sock:
            try:
                # Using the socket connect to a server...in this case localhost
                sock.connect(("localhost", 6060))

                thread_name = threading.current_thread().name
                # Send a message to the web server to supply a page as given by Host param of GET request
                msg = f"GET /{thread_name}/{i} HTTP/1.1\r\nHost: localhost\r\n Connection: close\r\n\r\n"
                sock.sendall(msg.encode("utf-8"))

                # Receive the data
                while (True):
                    data = sock.recv(1024)
                    print(f"Received: {data}")
                    if data == b'':
                        break
            except ConnectionError as e:
                print(e)
            except OSError as e:
                print(e)
            except Exception as e:
                print(e)

threads = []

for index in range(200):
    thread = threading.Thread(target=spam)
    thread.start()
    threads.append(thread)

for index in range(len(threads)):
    threads[index].join()
