from .commands import get_args
from .manager import run
import time
import sys

def main():
    run(**get_args())

if __name__ == "__main__":
    main()

