from time import sleep
from logging import error
from typing import Dict, List, Text

from nmap.nmap import PortScannerAsync
from Logger.log_action import Logger
from Logger.log_level import LogLevel
from Models.scan_result import ScanResult

import nmap
import threading
from typing import List, Dict

"""
    This class is responsible for nmap discoveries
"""

class NmapScanner:
    _logger = Logger("NmapScanner")
    _scan_results = []
    _aysnc_scan_thread_pool = list()

    def __init__(self, max_thread_count) -> None:
        try:
            self.__portScannerSync = nmap.PortScanner()
        except nmap.PortScannerError as error:
            # Nmap is not installed on the system
            self._logger.log(LogLevel.fatal, error.value)
            raise error
        self.__max_number_of_threads = max_thread_count
        self.__getNmapVersionOnSystem()
    
    def __getNmapVersionOnSystem(self):
        self.nmapVersion = self.__portScannerSync.nmap_version()
        self._logger.log(LogLevel.info, "Nmap version: {}".format(self.nmapVersion))


    def scan(self, target, isMultithreaded = False, ports = None, arguments = None):
        if isMultithreaded and self.__max_number_of_threads > 1:
            self._logger.log(LogLevel.info, "Starting multithreaded scan")
            return self.__initiateMultithreadedScan(target, ports, arguments)
        else:
            self._logger.log(LogLevel.info, "Starting sync scan")
            return self.__syncScan("-1", target, ports, arguments)

    def __syncScan(self, threadName, target, ports = None, arguments = None):
        self._logger.log(LogLevel.info, "Thread {} is started to search -{}:{}".format(threadName, target, ports))
        if arguments != None:
            result = self.__portScannerSync.scan(target, ports, arguments)
        else :
            result = self.__portScannerSync.scan(target, ports)
        
        
        self._scan_results.append(ScanResult(result))
        self._logger.log(LogLevel.info, "Thread {} Nmap scan result: {}".format(threadName, result['scan']))
        return self._scan_results

    def __initiateMultithreadedScan(self, target, ports = None, arguments = None):
        if self.__max_number_of_threads > 1:
            return self.__createThreads(target, ports, arguments)
        else:
            if arguments != None:
                result = self.__portScannerAsync.scan(target, ports, arguments)
            else :
                result = self.__portScannerAsync.scan(target, ports )
            
            self._scan_results.append(ScanResult(result))
            self._logger.log(LogLevel.info, "Nmap scan result: {}".format(result['scan']))

    def __createThreads(self, target, ports, arguments):
        [ports_begin, _, port_count] = self.__getPortsInfo(ports)
        if port_count != 1:
            number_of_ports_per_thread = port_count // self.__max_number_of_threads # integer division
            for i in range(self.__max_number_of_threads):
                port_range = "{}-{}".format(int(ports_begin) + number_of_ports_per_thread * i, int(ports_begin) + (i+1) * (number_of_ports_per_thread) - 1)
                thread = threading.Thread(target=self.__syncScan, args=(i, target, port_range, arguments), daemon=True)
                self._aysnc_scan_thread_pool.append(thread)
                thread.start()
            for thread in self._aysnc_scan_thread_pool:
                thread.join()
            return self._scan_results
        else:
            return self.__syncScan("-1", target, ports, arguments)
        

    def __getPortsInfo(self, ports: str):
        if ports != None:
            if ports.find('-') != -1:
                ports_splitted = ports.split('-')
                ports_begin = ports_splitted[0]
                ports_end = ports_splitted[1]
                return [ports_begin, ports_end, int(ports_end)  - int(ports_begin) + 1]
            else:
                return [0,0,1]
        else:
            return [0, (1 << 16) - 1, (1 << 16) - 1 ]# return 16 bit max int





