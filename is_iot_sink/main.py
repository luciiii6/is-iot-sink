from is_iot_sink.sink import Sink
import time
import sys

sink = Sink()

def main():
    sink.start()
    while sink.status() == True:
        time.sleep(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
