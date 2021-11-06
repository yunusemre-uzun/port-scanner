from nmap_scanner import NmapScanner
import logging

MAX_THREAD_COUNT = 4


def main():
    with open('Logs/portScanner.log', mode="w") as file:
         file.write("\n") # erase the log file
    logging.basicConfig(filename='Logs/portScanner.log', level=logging.INFO)
    nmapScanner = NmapScanner(MAX_THREAD_COUNT)
    result = nmapScanner.scan('127.0.0.1', False, '1-1000')
    return result


if __name__ == "__main__":
    main()
    