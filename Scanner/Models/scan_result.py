import json
import logging
from typing import Dict
from Models.syncronized_function import synchronized

class ScanResult:
    _host_dict  = {} # Dict<host, Dict<tcp/udp, Dict>>

    @synchronized
    def addResult(self, result):
        logging.info("Scan result: {}".format(result))
        command = result['nmap']['command_line']
        if command is None and result['nmap']['scaninfo']['error'] is not None:
            error_message = result['nmap']['scaninfo']['error']
            logging.error(error_message)
            self._host_dict["error"] = error_message
            return
        scan_started = result['nmap']['scanstats']['timestr']
        scanned_hosts = list(result['scan'].keys())
        scan_result = result['scan']
        for host in scanned_hosts:
            if host in self._host_dict:
                self.__addScanResultToHost(host, scan_result[host], command)
            else:
                status = scan_result[host]['status']
                self.__addNewHostWithScanResult(host, scan_result[host], scan_started, command, status)
                
    def __addScanResultToHost(self, host, scan_result, command=None):
        if command is not None:
            self._host_dict[host]['command'].append(command)
        if "osmatch" in scan_result and scan_result["osmatch"] != []:
            self._host_dict[host]['osmatch'] = scan_result["osmatch"]
        if 'tcp' in scan_result:
            if 'tcp' in self._host_dict[host]:
                self._host_dict[host]['tcp'].update(self.__getOpenPorts(scan_result['tcp'], 'tcp') )
            else:
                self._host_dict[host]['tcp'] = self.__getOpenPorts(scan_result['tcp'], 'tcp') 
        if 'udp' in scan_result:
            if 'udp' in self._host_dict[host]:
                self._host_dict[host]['udp'].update(self.__getOpenPorts(scan_result['udp'], 'udp') )
            else:
                self._host_dict[host]['udp'] = self.__getOpenPorts(scan_result['udp'], 'udp') 
    
    def __addNewHostWithScanResult(self, host, scan_result, scan_started, command, status):
        self._host_dict[host] = {"scan_started": scan_started, "command": [command], "status":  status}
        self.__addScanResultToHost(host, scan_result)

    def __getOpenPorts(self, ports_dict, port_type):
        ret = {}
        for key, value in ports_dict.items():
            if value['state'] == 'open':
                ret[key] = value
        return ret
    
    def addFinalResult(self, host, open_ports, scan_started):
        self._host_dict[host] = {"tcp": [open_ports], "scan_started": scan_started}

    def toJSON(self):
        ret_dict = self._host_dict.copy()
        """
        for host, result in self._host_dict.items():
            if ('tcp' not in result or result["tcp"] == {}) and\
                 ('udp' not in result or result["udp"] == {}):
                del ret_dict[host]
        """
        return ret_dict
    
    def onResponseSent(self):
        self._host_dict = {}
