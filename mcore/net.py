import asyncio
import json
import logging
import socket
from asyncio import StreamReader, StreamWriter
from json import JSONDecodeError
from threading import Lock
from typing import Any, Optional, Literal

from mcore.serialize import EnhancedJSONEncoder

logger = logging.getLogger(__name__)


class PacketJSONEncoder(EnhancedJSONEncoder):
    def default(self, o):
        if type(o) is Packet:
            return super().default(o.__dict__)
        return super().default(o)


# TODO support package in Network
class Packet(dict):
    def __init__(self, type: str, **kwargs):
        super().__init__(**kwargs)
        self.type = type

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        if type(value) is dict:
            value = Packet(**value)
        self[key] = value


class Network:
    BUFFER = 2
    ORDER: Literal["little", "big"] = 'big'

    def __init__(self, socket: socket.socket):
        self.socket = socket
        self._lock = Lock()

    def _recv(self) -> str:
        with self._lock:
            raw_length = self.socket.recv(self.BUFFER)
            length = int.from_bytes(raw_length, self.ORDER, signed=False)
            data = self.socket.recv(length)
            return data.decode()

    def _send(self, msg: str):
        with self._lock:
            data = msg.encode()
            length = int.to_bytes(len(data), self.BUFFER, self.ORDER, signed=False)
            self.socket.sendall(length)
            self.socket.sendall(data)

    def recv_json(self) -> Optional[dict]:
        data = self._recv()
        if not data:
            return None

        try:
            return json.loads(data)
        except JSONDecodeError:
            logger.exception(f'Could not parse data: {data}')
            return None

    def send_json(self, data: Any):
        self._send(json.dumps(data, cls=EnhancedJSONEncoder))

    def recv_pkg(self) -> Optional[Packet]:
        data = self.recv_json()

        if data is None:
            return None

        _type = data.pop('type')
        return Packet(_type, **data)

    def send_pkg(self, data: Packet):
        self.send_json(data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.socket.close()


class SecureNetwork(Network):
    def __init__(self, socket_: socket.socket, key: str):
        super().__init__(socket_)

        from cryptography.fernet import Fernet
        self.cipher_suite = Fernet(key.encode())

    # --- security layer
    def _recv(self) -> str:
        recv = super()._recv()
        if recv:
            return self.decrypt(recv)
        else:
            return ''

    def _send(self, msg: str):
        super()._send(self.encrypt(msg))

    # --- crypto
    @staticmethod
    def generate_key():
        from cryptography.fernet import Fernet
        return Fernet.generate_key().decode()

    def encrypt(self, text: str):
        return self.cipher_suite.encrypt(text.encode()).decode()

    def decrypt(self, cipher_text: str):
        return self.cipher_suite.decrypt(cipher_text.encode()).decode()


class AIONetwork:
    BUFFER = 2
    ORDER: Literal["little", "big"] = 'big'

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader: StreamReader = reader
        self.writer: StreamWriter = writer
        self._lock = asyncio.Lock()

    async def _recv(self) -> str:
        with self._lock:
            raw_length = await self.reader.read(self.BUFFER)
            length = int.from_bytes(raw_length, self.ORDER, signed=False)
            data = await self.reader.read(length)
            return data.decode()

    async def _send(self, msg: str):
        with self._lock:
            data = msg.encode()
            length = len(data).to_bytes(self.BUFFER, self.ORDER, signed=False)
            self.writer.write(length)
            self.writer.write(data)
            await self.writer.drain()

    async def _recv_json(self) -> Optional[dict]:
        data = await self._recv()
        if data:
            return json.loads(data)
        else:
            return None

    async def _send_json(self, data: Any):
        await self._send(json.dumps(data, cls=EnhancedJSONEncoder))

    async def recv_pkg(self) -> Optional[Packet]:
        data = await self._recv_json()
        if data:
            _type = data.pop('type')
            return Packet(_type, **data)

        return None

    async def send_pkg(self, data: Packet):
        await self._send_json(data)

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
