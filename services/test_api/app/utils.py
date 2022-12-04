#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time
from datetime import datetime


def is_socket_open(*, host: str, port: int, timeout: int = 3) -> bool:
    """
    Check if specified socket available
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        print_msg(f'Trying to connect to the host({host}) port({port})')
        sock.connect((host, port))
        sock.shutdown(socket.SHUT_RDWR)
        return True
    except socket.error as error:
        print_msg(f'Socket({host}:{port}) connection error:  {error}')
        return False
    finally:
        sock.close()


def is_service_running(*, host: str, port: int, retry: int = 10, delay: int = 10) -> bool:
    """
    Try to achive specified target several times
    """
    is_online = False
    for i in range(retry):
        print_msg(f'Discovering service on {host}:{port}. Try: {i}/{retry}')
        if is_socket_open(host=host, port=port):
            is_online = True
            break
        time.sleep(delay)
    return is_online


def get_current_time():
    """
    Returns current datetime (!!!not utc!!!) in appropriate view
    """
    return datetime.now().strftime('[%d %b %Y %H:%M:%S]')


def print_msg(msg: str) -> None:
    """
    Default print wrapper that prints provided msg with datetime prefix
    """
    print(f'{get_current_time()}    {msg}')
