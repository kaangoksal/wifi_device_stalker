import datetime
from threading import Timer


class AccessPoint(object):
    # TODO create DB modelz

    def __init__(self, bssid, ssid, channel):
        self.bssid_address = bssid
        self.ssid = ssid
        self.channel = channel

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

    def __str__(self):
        return "Client with mac " + str(self.mac_address) + " <------> " + str(self.connected_access_point)

    def __hash__(self):
        """
        We need a good hasghing algo to combine the found clients,
        we hope that mac addresses are unique, if not we are fucked
        :return:
        """
        mac_string = self.mac_address

        return mac_string.__hash__()

    def __eq__(self, other):
        if isinstance(other, WifiClient):
            return self.mac_address == other.mac_address
        else:
            return False


class WifiClientSession(object):
    # TODO finish exceptions

    def __init__(self, client_object):

        self.client = client_object.mac_address
        self.session_start = None
        self.session_stop = None

        self.session_extend = False
        self.session_time = 300  # this is in seconds
        self.session_timer = None

        self.connected_access_points = [] #this should include the time of spotting
        self.current_access_point = None

        self.spotted_channels = [client_object.channel] # this is also going to be time vs channel
        self.current_channel = None

        self.observed_power_levels = [] # this is going to be time vs power level pair
        self.current_power_level = None

    def parse_data(self, client_object):
        if client_object is None:
            raise Exception("None client object is not allowed")

        # TODO check client object data to add acccess points and such..

    def record_connected_access_point(self, access_point):
        """
        Records connected access point to object
        :param access_point: the bssid of the access point that is connected
        :return:
        """
        if access_point is not None:
            raise Exception("access point cannot be null")
        if self.session_stop is not None:
            raise Exception("Session is closed! cannot add access point")
        if self.current_access_point == access_point:
            pass
        else:
            self.connected_access_points.append((access_point, datetime.datetime.now()))

    def record_spotted_channel(self, channel):
        """
        Records the spotted channel to the session with the time
        :param channel: the channel number as int
        :return:
        """
        if self.current_channel == channel:
            pass
        else:
            self.spotted_channels.append((channel, datetime.datetime.now()))

    def record_rssi(self, rssi):
        """
        Records the signal strength
        :param rssi: observed signal strength as interger
        :return:
        """
        self.observed_power_levels.append((rssi, datetime.datetime.now()))

    def stop_session(self):
        """
        Stops the session and records the session stop time
        :return:
        """
        if self.session_stop is not None:
            raise Exception("Session is already closed")
        self.session_stop = datetime.datetime.now()

    def continue_session(self):
        """
        This method raises the flag which will let the session get extended for 5 more mintes (hardcoded). It should be
        called whenever the client is heard again!
        :return:
        """
        self.session_extend = True

    def check_session_expiry(self):
        """
        This function is for the timer thread which counts down from 5 mins and after that decides whether the client
        is gone or not. If we don't hear anything from the client for 5 minutes, we assume that it is gone and the session
        can be closed.
        :return:
        """
        if self.session_extend:
            self.session_extend = False
            self.session_timer = Timer(self.session_time, self.check_session_expiry)
        else:
            self.stop_session()


class WifiAcessPointSession(object):
    # TODO finish exceptions

    def __init__(self, access_point):

        self.bssid = access_point.bssid_address
        self.session_start = None
        self.session_stop = None

        self.session_extend = False
        self.session_time = 300  # this is in seconds
        self.session_timer = None

        self.connected_clients = []  # this should include the time of spotting
        #self.current_clients = [] # the list of currently connected clients... WTF... a little too ambitious for this stage

        self.spotted_channels = [access_point.channel]  # this is also going to be time vs channel
        self.current_channel = access_point.channel

        self.observed_power_levels = []  # this is going to be time vs power level pair
        self.current_power_level = None

    def parse_data(self, acces_point_object):
        if acces_point_object is None:
            raise Exception('access point object cannot be null')
        self.session_extend = True

        #TODO check the channels, power level, connected clients!


    def record_connected_client(self, client_mac):
        """
        Records connected access point to object
        :param client_mac: the mac address of the client that is connected to the access point
        :return:
        """
        if client_mac is not None:
            raise Exception("client mac address cannot be null")
        if self.session_stop is not None:
            raise Exception("Session is closed! cannot add connected client")
        else:
            self.connected_clients.append((client_mac, datetime.datetime.now()))

    def record_spotted_channel(self, channel):
        """
        Records the spotted channel to the session with the time
        :param channel: the channel number as int
        :return:
        """
        if self.current_channel == channel:
            pass
        else:
            self.spotted_channels.append((channel, datetime.datetime.now()))

    def record_rssi(self, rssi):
        """
        Records the signal strength
        :param rssi: observed signal strength as interger
        :return:
        """
        self.observed_power_levels.append((rssi, datetime.datetime.now()))

    def stop_session(self):
        """
        Stops the session and records the session stop time
        :return:
        """
        if self.session_stop is not None:
            raise Exception("Session is already closed")
        self.session_stop = datetime.datetime.now()

    def continue_session(self):
        """
        This method raises the flag which will let the session get extended for 5 more mintes (hardcoded). It should be
        called whenever the client is heard again!
        :return:
        """
        self.session_extend = True

    def check_session_expiry(self):
        """
        This function is for the timer thread which counts down from 5 mins and after that decides whether the client
        is gone or not. If we don't hear anything from the client for 5 minutes, we assume that it is gone and the session
        can be closed.
        :return:
        """
        if self.session_extend:
            self.session_extend = False
            self.session_timer = Timer(self.session_time, self.check_session_expiry)
        else:
            self.stop_session()











