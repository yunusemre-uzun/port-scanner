from datetime import datetime

class ScanRequestModel:
    def __init__(self, host, port_selection, ports_begin, ports_end, arguments, os_scan) -> None:
        self._host = host
        self.port_selection = port_selection
        self._ports_begin = ports_begin
        self._ports_end = ports_end
        self._arguments = arguments
        self._os_scan = os_scan
    
    def __getPortsString(self) -> str:
        if self.port_selection == 'portRange':
            return "{}-{}".format(self._ports_begin, self._ports_end)
        elif self.port_selection == 'singlePort':
            return "{}".format(self._ports_begin)
        elif self._os_scan:
            return str(None)
        else:
            return "{}-{}".format(1, (1 << 16) - 1)
    
    def createScanRequest(self) -> str:
        return {'name': datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '-' + self._host,'host': self._host, 'ports': self.__getPortsString(), 'arguments': self._arguments, 'os_scan': self._os_scan}