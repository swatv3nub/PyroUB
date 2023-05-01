import socket

async def netcat(host, port, content):
    meow = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    meow.connect((host, port))
    meow.sebdall(content.encode())
    meow.shutdown(socket.SHUT_WR)
    while True:
        data = meow.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    meow.close()
    
async def paste(content):
    link = await netcat("ezup.dev", 9999, content)
    return link
