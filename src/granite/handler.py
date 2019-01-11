import socket
from curio import Queue
from granite.request import Channel, Request
from granite.response import Response, response_handler
from granite.http import HTTPStatus, HTTPError


async def request_handler(app, client, addr):
    try:
        async with client:
            try:
                async for request in Channel(client):
                    response = await app(request)
                    await response_handler(client, response)
            except HTTPError as exc:
                await client.sendall(bytes(exc))
    except (ConnectionResetError, BrokenPipeError, socket.timeout):
        # The client disconnected or the network is suddenly
        # unreachable.
        pass