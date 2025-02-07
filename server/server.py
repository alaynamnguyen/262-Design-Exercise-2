import socket
import selectors
import types
import configparser
import json
from model import User
from controller.login import handle_login_request

# Load config
config = configparser.ConfigParser()
config.read("../config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

sel = selectors.DefaultSelector()

# TODO BEGIN get rid of this hardcoded code
import hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

hardcoded_accounts = [("yinan", "pass1"), ("alayna", "pass2")]
accounts_dict = dict()
users = []
for account in hardcoded_accounts:
    user = User(username=account[0], password=account[1])
    accounts_dict[user.uid] = { "username": account[0], "password": hash_password(account[1]) }
print("Accounts:", accounts_dict)
# TODO END get rid of this hardcoded code

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
            data.inb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()

        print("Received DATA:", data.inb)
        if data.inb:
            message = json.loads(data.inb.decode("utf-8"))
            if message["task"].startswith("login"):
                print("Calling handle_login_request")
                handle_login_request(data, message, accounts_dict, users)
                print("Accounts", accounts_dict, "Users", users)
            # TODO handle the other types of tasks
            # elif message == "count":
            #     data.outb += str(len(message.split())).encode("utf-8")
            data.inb = b""
        
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

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
