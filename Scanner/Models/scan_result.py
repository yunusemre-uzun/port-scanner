import json
from typing import Dict

class ScanResult:
    _host_dict  = {} # Dict<host, Dict<tcp/udp, Dict>>
    
    def addResult(self, result):
        command = result['nmap']['command_line']
        scan_started = result['nmap']['scanstats']['timestr']
        scanned_hosts = list(result['scan'].keys())
        scan_result = result['scan']
        for host in scanned_hosts:
            if host in self._host_dict:
                self.__addScanResultToHost(host, scan_result[host])
            else:
                self.__addNewHostWithScanResult(host, scan_result[host], scan_started, command)
                
    def __addScanResultToHost(self, host, scan_result):
        if 'tcp' in scan_result:
            if 'tcp' in self._host_dict[host]:
                self._host_dict[host]['tcp'].update(scan_result['tcp'])
            else:
                self._host_dict[host]['tcp'] = scan_result['tcp']
        if 'udp' in scan_result:
            if 'udp' in self._host_dict[host]:
                self._host_dict[host]['udp'].update(scan_result['udp'])
            else:
                self._host_dict[host]['udp'] = scan_result['udp']
    
    def __addNewHostWithScanResult(self, host, scan_result, scan_started, command):
        self._host_dict[host] = {"scan_started": scan_started, "command": command}
        self.__addScanResultToHost(host, scan_result)

    
    def toJSON(self):
        return self._host_dict
