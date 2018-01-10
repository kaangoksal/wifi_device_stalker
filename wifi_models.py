class AccessPoint(object):
    # TODO create DB modelz

    def __init__(self, bssid, ssid, channel):
        self.bssid_address = bssid
        self.ssid = ssid
        self.channel = channel
        self.first_seen = None
        self.seen_history = []

    def __str__(self):
        return "Wifi Access point " + str(self.ssid) + "with bssid address " + str(self.bssid_address)

    def __hash__(self):
        """
        We need a good hasghing algo to combine the found access pints,
        we hope that mac addresses are unique, if not we are fucked
        :return:
        """
        bssid_string = self.bssid_address

        #the hash calls the original has function
        return bssid_string.__hash__()

    def __eq__(self,other):
        if isinstance(other, AccessPoint):
            return self.bssid_address == other.bssid_address
        else:
            return False


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

    def __hash__(self):
        """
        We need a good hasghing algo to combine the found clients,
        we hope that mac addresses are unique, if not we are fucked
        :return:
        """
        mac_string = self.mac_address

        return mac_string.__hash__()

    def __eq__(self,other):
        if isinstance(other, WifiClient):
            return self.mac_address == other.mac_address
        else:
            return False



