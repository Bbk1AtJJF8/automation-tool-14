import re
import socket
from typing import Any, Optional

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def is_valid_port(port: Any) -> bool:
    try:
        return 1 <= int(port) <= 65535
    except (ValueError, TypeError):
        return False

def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0

def sanitize_path(path: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_/.-]', '', path).lstrip('/')

def validate_json_schema(data: dict, keys: list) -> bool:
    return all(k in data for k in keys)

def coerce_boolean(value: Any) -> bool:
    if isinstance(value, bool): return value
    return str(value).lower() in ('true', '1', 't', 'y', 'yes')