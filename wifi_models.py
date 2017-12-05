class AccessPoint(object):
    # TODO create DB modelz

    def __init__(self, bssid, ssid, channel):
        self.mac_address = bssid
        self.ssid = ssid
        self.channel = channel
        self.first_seen = None
        self.seen_history = []

    def __str__(self):
        return "Wifi Access point " + str(self.ssid) + "with mac address " + str(self.mac_address)


class WifiClient(object):
    # TODO create DB Modelz

    def __init__(self, mac_address, channel):
        self.mac_address = mac_address

        self.connected_access_point = None
        self.channel = channel

        self.first_seen = None
        self.seen_history = []

    def __str__(self):
        return "Client with mac " + str(self.mac_address)


