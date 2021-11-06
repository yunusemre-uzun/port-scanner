class ScanRequestModel:
    def __init__(self, host, port_selection, ports_begin, ports_end, arguments) -> None:
        self._host = host
        self.port_selection = port_selection
        self._ports_begin = ports_begin
        self._ports_end = ports_end
        self._arguments = arguments
    
    def __getPortsString(self) -> str:
        if self.port_selection == 'portRange':
            return "{}-{}".format(self._ports_begin, self._ports_end)
        elif self.port_selection == 'singlePort':
            return "{}".format(self._ports_begin)
        else:
            return "{}-{}".format(1, (1 << 16) - 1)
    
    def createScanRequest(self) -> str:
        return {'host': self._host, 'ports': self.__getPortsString(), 'arguments': self._arguments}