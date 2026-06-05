"""Application entry point.

`obfy build --src ./src` mirrors this file to ./dist/run.py as a self-activating
stub, and PyInstaller bundles that stub as the executable's entry point.
"""

import sys

from app import greet


def main() -> int:
    name = sys.argv[1] if len(sys.argv) > 1 else "world"
    print(greet(name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
