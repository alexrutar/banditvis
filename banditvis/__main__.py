from .commands import get_args
from .manager import run
import time
import sys


if __name__ == "__main__":
    run(**get_args())

