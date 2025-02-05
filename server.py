import socket
import selectors
import types
import configparser

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

sel = selectors.DefaultSelector()

def trans_to_pig_latin(text):
    words = text.split()
    pig_latin_words = []
    for word in words:
        if word[0] in "aeiou":
            pig_latin_words.append(word + "way")
        else:
            pig_latin_words.append(word[1:] + word[0] + "ay")
    return " ".join(pig_latin_words)

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            command = recv_data.decode("utf-8").strip()
            words = command.split()
            
            if words[0] == "count":
                response = str(len(words) - 1)
            elif words[0] == "translate":
                response = trans_to_pig_latin(" ".join(words[1:]))
            else:
                response = "Unknown command"

            sock.send(response.encode("utf-8"))  # Send the response immediately
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()

if __name__ == "__main__":
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print(f"Listening on {HOST}:{PORT}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()
