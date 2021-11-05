class ScanResult:
    def __init__(self, result) -> None:
        self.command = result['nmap']['command_line']
        self.scanDuration = result['nmap']['scanstats']['elapsed']
        self.upHostCount = result['nmap']['scanstats']['uphosts']
        self.scanStarted = result['nmap']['scanstats']['timestr']
        self.scannedHosts = list(result['scan'].keys())
        self.scanResult = result['scan']
