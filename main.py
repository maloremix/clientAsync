import asyncio
import random
from datetime import datetime
import logger

def get_time():
    s = datetime.now().isoformat(" ", timespec='milliseconds')
    return f"{s[:10]};{s[10:]}"

def closure_for_log():
    time = None
    message_send = None
    message_accept = None
    async def tcp_echo_client():
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888)
        read_task = asyncio.create_task(read(reader))
        write_task = asyncio.create_task(write(writer))
        await read_task
        await write_task

    async def read(reader):
        nonlocal message_accept
        while True:
            message_code = await reader.readline()
            message_accept = message_code.decode(encoding='ascii')
            if "KEEPALIVE" not in message_accept:
                logger.log_client(time, message_send, message_accept)
            else:
                logger.log_client(time, message_send, message_accept, True)

    async def write(writer):
        count = 0
        nonlocal time, message_send
        while True:
            message_send = "[{count}] PING".format(count=count)
            s = bytearray(message_send.encode(encoding='ascii'))
            s.append(0x0A)
            writer.write(s)
            time = get_time()
            await writer.drain()
            count+=1
            interval = random.randint(300, 3000)
            await asyncio.sleep(float(interval)/1000)
    return tcp_echo_client

tcp_echo_client = closure_for_log()
asyncio.run(tcp_echo_client())