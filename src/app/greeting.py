"""Your protected business logic goes here.

Everything under src/ is obfuscated and AES-256-GCM encrypted by `obfy build`
before PyInstaller ever sees it, so this source never ships in the final binary.
"""

from datetime import datetime


def greet(name: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Hello, {name}! This code is protected by obfy. ({now})"
