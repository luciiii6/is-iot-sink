from is_iot_sink.sink import Sink
from is_iot_sink.logger import LOG
import time
import sys
import signal

sink = Sink()

def signal_handler(sig, frame):
    LOG.info("SIGINT received!")
    sink.stop()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    sink.start()
    while sink.status() == True:
        time.sleep(1)
    
if __name__ == "__main__":
    main()
