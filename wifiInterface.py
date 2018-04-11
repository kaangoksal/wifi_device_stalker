from scapy.all import *

from scapy.layers.dot11 import *
from threading import Thread
import time
from queue import Queue
from models.wifi_models import WifiClient, AccessPoint
from wifi_tool_wrappers import ipWrapper, iwconfigWrapper, iwlistWrapper, iwWrapper, wifiModes
import enum


class DeviceStatus(enum.Enum):
    """
    This class is for the status of the wifi interface. This can be grately increased...
    """

    not_ready = "not ready"
    searching_all_channels = "searching_all_channels"
    ready = "ready"


class wifi_device_sniffer_Interface(object):

    def __init__(self, device_name, interface_name):
        """
        This function registers a wifi device...
        :param device_name: name of the device (this is for human use)
        :param interface_name: the system interface name of the device, we need this so we can
        switch modes and hop channels
        """

        self.channel = 0
        self.channels = iwlistWrapper.get_channels(interface_name)

        self.device_name = device_name
        self.interface_name = interface_name

        self.mode = None
        self.logger = None

        self.channel_hop_thread = None
        self.collect_packets_thread = None

        self.status = DeviceStatus.not_ready

        self.found_devices = Queue()

    def start_searching(self):
        """
        This function creates and starts the threads that monitor and help through channels
        :return:
        """
        if self.status != DeviceStatus.searching_all_channels:
            if self.mode == wifiModes.monitor:

                print("Threads firing up! ")
                self.channel_hop_thread = Thread(target=self.channel_hop)
                self.collect_packets_thread = Thread(target=self.collect_packets)
                self.channel_hop_thread.start()
                self.collect_packets_thread.start()
                print("Threads online!")
                self.status = DeviceStatus.searching_all_channels

            else:
                self.logger.error("Interface is not in monitor mode!")
        else:
            print("Already searching for devices! Can't fire up twice")

    def collect_packets(self):
        """
        This function collects packets and filters them. This is a blocking call!
        :return: does not return
        """
        sniff(iface=self.interface_name, store=0, prn=self.filter_clients_and_access_points)

    def channel_hop(self):
        """
        This method hops channels!
        :return: nothing! it is an infinite loop
        """
        while self.status == DeviceStatus.searching_all_channels:
            for channel in self.channels:
                iwWrapper.set_channel(self.interface_name, channel)
                time.sleep(0.5)

    def start_wifi_monitor_mode(self):
        """
        This function switches to interface into monitor mode, first it switches back to managed mode and then switches
        it back to monitor. I encountered weird bugs while just switching to monitor without first switching to managed
        maybe it is just my chipset but this works all the time.
        :return: true if the attempt was successful, false if it has failed
        """
        print("Will try to activate monitor mode")
        # Nothin would be bad if the users tries to switch to
        # monitor again so we can leave it as it is. no need to check
        try:
            wait = 1
            ipWrapper.link_down(self.interface_name)
            time.sleep(wait)
            iwconfigWrapper.set_mode(self.interface_name, "managed")
            time.sleep(wait)
            ipWrapper.link_up(self.interface_name)
            time.sleep(wait)
            print("Managed Mode Activated")
            ipWrapper.link_down(self.interface_name)
            time.sleep(wait)
            iwconfigWrapper.set_mode(self.interface_name, "monitor")
            time.sleep(wait)
            ipWrapper.link_up(self.interface_name)
            print("Monitor Mode Activated")
            self.mode = wifiModes.monitor
            self.status = DeviceStatus.ready
            return True
        except Exception:
            print("Error switching to monitor mode")
            return False
            # TODO log error

    def switch_to_managed_mode(self):
        #  Nothing bad would happen if the user switches to
        # managed mode again from managed mode, so we don't need to check
        try:
            ipWrapper.link_down(self.interface_name)
            iwconfigWrapper.set_mode(self.interface_name, "managed")
            ipWrapper.link_up(self.interface_name)
            self.mode = wifiModes.managed
            self.status = DeviceStatus.not_ready
        except Exception:
            sys.exit('Could not start monitor mode')

    def access_point_add(self, packet, channel):
        ssid = packet[Dot11Elt].info
        bssid = packet[Dot11].addr3.lower()

        new_acces_point = AccessPoint(bssid, ssid, channel)

        self.found_devices.put(new_acces_point)

    @staticmethod
    def noise_filter(skip, addr1, addr2):
        # Broadcast, broadcast, IPv6mcast, spanning tree, spanning tree, multicast, broadcast
        ignore = ['ff:ff:ff:ff:ff:ff', '00:00:00:00:00:00', '33:33:00:', '33:33:ff:', '01:80:c2:00:00:00', '01:00:5e:']
        if skip:
            ignore += [addr.lower() for addr in skip]
        for i in ignore:
            if i in addr1 or i in addr2:
                return True

    def client_add(self, addr1, addr2, channel):
        new_client = WifiClient(addr2, channel)
        new_client.connected_access_point = addr1

        self.found_devices.put(new_client)

    def filter_clients_and_access_points(self, packet):
        print(type(packet))
        print(type(packet.payload.payload))
        print("Address 1: ", packet.addr1)
        print("Address 2: ", packet.addr2)
        print("Address 3: ", packet.addr3)
        
        print("=============================")
        print(packet)
        print("=============================")

        if packet.haslayer(Dot11):
            if packet.addr1 and packet.addr2:
                packet.addr1 = packet.addr1.lower()
                packet.addr2 = packet.addr2.lower()

                if packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeResp):
                    self.access_point_add(packet, self.channel)

                if self.noise_filter([], packet.addr1, packet.addr2):
                    return

                # Management = 1, data = 2
                if packet.type in [1, 2]:
                    self.client_add(packet.addr1, packet.addr2, self.channel)
