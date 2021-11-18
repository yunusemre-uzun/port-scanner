import socket
import logging

from threading import Thread
from queue import Queue
from datetime import datetime

from Models.scan_result import ScanResult

class PortScanner:
    def __init__(self, host: str, ports: str) -> None:
        self.ports_to_be_scanned = ports
        self.host_to_be_scanned = host
        self.open_ports = {}
        self._createQueue()
        self._createThreads()

    def _createQueue(self):
        self.__port_queue = Queue()

    def _createThreads(self):
        for x in range(16):
            t = Thread(target=self._threader, daemon=True)
            t.start()
    
    def _getPortsBoundaries(self):
        if self.ports_to_be_scanned.find("-") != -1:
            ports_begin, ports_end = self.ports_to_be_scanned.split("-")
            return (int(ports_begin), int(ports_end))
        else:
            return  (int(self.ports_to_be_scanned), int(self.ports_to_be_scanned)+1)
    
    def _scan(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            
            # returns an error indicator
            result = s.connect_ex((self.host_to_be_scanned,port))
            if result ==0:
                logging.info("Port {} is open for host {}".format(port, self.host_to_be_scanned))
                self.open_ports[port] = {"state": "open"}
            s.close()
        except socket.gaierror:
            logging.error("Hostname could not be resolved. Exiting")
            return

    def _threader(self):
        while True:
            port = self.__port_queue.get()
            self._scan(port)
            self.__port_queue.task_done()
    
    def scan(self):
        self._scan_started = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        (ports_begin, ports_end) = self._getPortsBoundaries()
        for port in range(ports_begin, ports_end):
            self.__port_queue.put(port)
        self.__port_queue.join()
        return self._createResult()
    
    def _createResult(self):
        scan_result = ScanResult()
        scan_result.addFinalResult(self.host_to_be_scanned, self.open_ports, self._scan_started)
        return scan_result
