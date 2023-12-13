import argparse
import logging
from .config import *

from .app import app

LOCAL_IP = LOCAL_IP
LOCAL_PORT = API_PORT


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--debug", action="store_true", help="enable debug logging")
    parser.add_argument("-i", "--local-ip", type=str, default=LOCAL_IP, help="local IP on which to listen")
    parser.add_argument("-p", "--port", type=int, default=LOCAL_PORT, help="port on which to listen")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s")

    app.run(host=args.local_ip, port=args.port, debug=args.debug)
