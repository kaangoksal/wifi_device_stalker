from wifiInterface import wifi_device_sniffer_Interface
from wifi_tool_wrappers import iwconfigWrapper
from models.wifi_models import WifiClient, AccessPoint, WifiAcessPointSession, WifiClientSession
import os
import time
from threading import Thread


class main:
    def __init__(self):
        self.client_sessions = {}
        self.access_point_sessions = {}


        self.status = 1

        interface_to_use = self.select_wifi_interface()

        # We are creating a wifi device sniffer interface
        self.start_sniffing_with_device(interface_to_use)

        #  TODO think about displaying the data somehow... either tkinter or some web shit...


        # while 1:
        #     time.sleep(1)
        #     os.system('clear')
        #     print(len(self.found_devices))
        #     #self.print_devices()
        #     #self.print_aps()

    def start_sniffing_with_device(self, device):
        """
        Switches the device to monitor mode and starts capturing packets with it.
        :param device: the device object, NOT THE STRING DEVICE NAME
        :return: nothing
        """
        selected_interface = wifi_device_sniffer_Interface("Sniff1", device)
        selected_interface.start_wifi_monitor_mode()
        selected_interface.start_searching()


        device_thread = Thread(target=self.device_loop, args=[selected_interface])
        device_thread.start()
        print("Device ", device, " started sniffing")

    def select_wifi_interface(self):
        """
        This is for user to choose which Wifi interface that he/she is going to use for scanning, right now it only
        supports single interface, in near future I will add support for multiple interfaces.
        :return: name of the interaface that the user have selected
        """
        available_wifi_interfaces = iwconfigWrapper.get_wifi_interfaces()

        print("Select wifi interface to use")
        print("===============================")
        i = 1
        for wifi_interface_name in available_wifi_interfaces:
            print(str(i) + ") " + wifi_interface_name)
            i += 1

        user_selection = int(input()) - 1
        print("Returning ", available_wifi_interfaces[user_selection])
        return available_wifi_interfaces[user_selection]

    def device_loop(self, device):
        """
        This method will continuously poll the device, the collect_data_from_interface method is actually a blocking call
        so this should not cause a CPU spin.
        :param device:
        :return:
        """
        #print("Device loop started")
        while self.status:
            self.collect_data_from_interface(device)
        #print("Device loop terminated")

    def collect_data_from_interface(self, interface):
        """
        This should collect data from the device and push it to the set.
        :param interface: the interface that we are probing
        :return:
        """
        #print("waiting on the queue")
        new_device = interface.found_devices.get()

        #print("Found new device!")

        # We should organize the data!
        if type(new_device) == AccessPoint:
            # todo check whether this is the first time witnessing this access point and record that to the sql
            access_point_session = self.access_point_sessions.get(new_device.bssid_address, None)
            if access_point_session is None:
                # This means that this is the first session (as of current timeframe = 5 mins) that we are experiencing
                # with this access point, therefore we need to open a new session!
                access_point_session = WifiAcessPointSession(new_device)
                self.access_point_sessions[new_device.bssid_address] = access_point_session
            else:
                access_point_session.parse_data(new_device)

        elif type(new_device) == WifiClient:
            # TODO check whether this is the first time witnessing this client and also record that to the sql
            client_session = self.client_sessions.get(new_device.mac_address, None)
            if client_session is None:
                # This means that we are seeing this client newly! (as of current timeframe = 5mins) so we should
                # open a new client session and record the stuff that we are collecting about this client
                client_session = WifiClientSession(new_device)
                self.client_sessions[new_device.mac_address] = client_session
            else:
                client_session.parse_data(new_device)


    # def print_devices(self):
    #     print("===========Clients==============")
    #     for device in list(self.found_devices):
    #         print(device)
    #
    # def print_aps(self):
    #     print("===============APs=================")
    #     for ap in list(self.found_access_points):
    #         print(ap)


new_pp = main()



