from wifiInterface import wifi_device_sniffer_Interface
from wifi_tool_wrappers import iwconfigWrapper, iwWrapper, ipWrapper, iwlistWrapper
from wifi_models import WifiClient, AccessPoint
import os
import time
from threading import Thread


class main:
    def __init__(self):
        self.found_devices = set()
        self.found_access_points = set()
        self.status = 1

        interface_to_use = self.select_wifi_interface()

        # We are creating a wifi device sniffer interface
        selected_interface = wifi_device_sniffer_Interface("Sniff1", interface_to_use)
        selected_interface.start_wifi_monitor_mode()
        selected_interface.start_searching()

        device_thread = Thread(target=self.device_loop, args=[selected_interface])
        device_thread.start()
        print("Started the device Thread")
        while 1:
            time.sleep(1)
            os.system('clear')
            print(len(self.found_devices))
            self.print_devices()

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
        This method will contionusly poll the device, the collect_data_from_interface method is actually a blocking call
        so this should not cause a CPU spin.
        :param device:
        :return:
        """
        print("Device loop started")
        while self.status:
            self.collect_data_from_interface(device)
        print("Device loop terminated")

    def collect_data_from_interface(self, interface):
        """
        This should collect data from the device and push it to the set.
        :param interface: the interface that we are probing
        :return:
        """
        #print("waiting on the queue")
        new_device = interface.found_devices.get()

        #print("Found new device!")
        if type(new_device) == AccessPoint:
            self.found_access_points.add(new_device)

        elif type(new_device) == WifiClient:
            self.found_devices.add(new_device)

    def print_devices(self):
        print("===========New Result==============")

        for device in list(self.found_devices):
            print(device)


new_pp = main()



