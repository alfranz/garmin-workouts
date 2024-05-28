import os
import sys
from pytest_socket import disable_socket

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def pytest_runtest_setup():
    disable_socket()
